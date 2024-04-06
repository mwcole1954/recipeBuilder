import json
import os
import pathlib
import urllib.error
from urllib import request
from bs4 import BeautifulSoup
from collections import defaultdict

import message_dialog
import simple_dialog
import ssl


class Import:
    """Gets, Cleans and Saves recipe data
    initialize Import
    call start_import()
    """
    # This makes it work on Mac (Not sure how it works, but it is needed)
    ssl._create_default_https_context = ssl._create_unverified_context

    base_data = {
        'header': ['description', 'author'],
        'summary': ['prepTime', 'cookTime', 'totalTime', 'recipeYield', 'recipeCategory', 'recipeCuisine'],
        'ingredients': 'recipeIngredient',  # list
        'nutrients': 'nutrition',  # dict
        'instructions': 'recipeInstructions',  # list of dicts
    }

    cleaner = {
        'Time': ' time',
        'recipe': '',
        'PT': '',
        'Content': '',
        'Fat': ' fat',
        '; ': ', ',
    }

    file_names = ['header', 'summary', 'ingredients', 'nutrients', 'instructions']

    def __init__(self):
        self.abort = False
        self.data = None
        self.def_dict = defaultdict()  # Dict contains the recipe data, key: value
        self.website = ""
        self.num = None
        self.recipe_title = None
        self.recipe_saved = False
        self.gen = self.counter()

    def check_directory(self):
        directory = pathlib.Path(os.getcwd(), "Recipes", self.recipe_title)
        while directory.exists():
            change_recipe_name = simple_dialog.ask_strings("Change Recipe Name",
                                                           "Recipe Name exists. Enter a new name: ",
                                                           default_val=f"{self.recipe_title}")
            change_recipe_name = change_recipe_name[0]
            if change_recipe_name != 'Cancel':
                if self.recipe_title.strip().lower() != change_recipe_name.strip().lower():
                    self.recipe_title = change_recipe_name
                    directory = pathlib.Path(os.getcwd(), "Recipes", self.recipe_title)
            else:
                return None
        directory.mkdir(exist_ok=False)
        return directory

    @classmethod
    def clean_data(cls, d):
        if d:
            for k, v in Import.cleaner.items():
                if not isinstance(d, int):
                    if d.find(k) >= 0:
                        d = d.replace(k, v)
            return d

    def json_walk(self, item=''):
        if isinstance(item, list):
            self.walk_list(item)
        if isinstance(item, dict):
            self.walk_dict(item)

    def walk_list(self, list_item):
        for item in list_item:
            self.json_walk(item)

    def walk_dict(self, dict_item):
        for key in dict_item:
            if key in self.def_dict:
                num = next(self.gen)  # counter generator
                self.def_dict[f"{key}{num}"] = dict_item[key]
            else:
                self.def_dict[key] = dict_item[key]
            self.json_walk(dict_item[key])
            # print(self.def_dict[key])

    def get_recipe_title(self):
        if self.website != '':
            if self.website.find('?') > -1:
                self.website = self.website[:self.website.find("?")]
            url_parts = self.website.rstrip('/').strip().split('/')[-1]
            url_parts = url_parts.replace('-', ' ').split()
            self.recipe_title = ''
            for part in url_parts:
                if not part.isnumeric():
                    self.recipe_title += f"{part} "
            self.recipe_title = self.recipe_title.replace('recipe', '').strip()

    def get_recipe_files(self):
        header, summary, ingredients, nutrients, instructions = '', '', '', '', ''
        for key, value in Import.base_data.items():
            if key == 'header':
                header = f"{self.recipe_title};"
                for item in value:
                    header += f" {self.def_dict.get(item)}"
            elif key == 'summary':
                for item in Import.base_data[key]:  # The desired keys
                    if isinstance(self.def_dict.get(item), list):  # The recipe data
                        summary += f"{self.clean_data(item)}; "
                        for it in self.def_dict.get(item):
                            summary += f"{self.clean_data(it)}, "
                            print(summary)
                        summary = summary.strip(', ')
                        summary += f"\n"
                    else:
                        summary += f"{self.clean_data(item)}; {self.clean_data(self.def_dict.get(item))}\n"
            elif key == 'ingredients':
                if self.def_dict.get(Import.base_data[key]):
                    for num, item in enumerate(self.def_dict.get(Import.base_data[key])):
                        ingredients += f"{num + 1}; {item}\n"
            elif key == 'nutrients':
                if self.def_dict.get(Import.base_data[key]):
                    for k, v in self.def_dict.get(Import.base_data[key]).items():
                        if k.find("@") < 0:
                            nutrients += f"{self.clean_data(k)}; {self.clean_data(v)}\n"
            elif key == 'instructions':
                if self.def_dict.get(Import.base_data[key]):
                    for num, item in enumerate(self.def_dict.get(Import.base_data[key])):
                        if isinstance(item, dict):
                            instructions += f"{num + 1}; {self.clean_data(item.get('text'))}\n"
                        elif isinstance(item, str):
                            instructions += f"{num + 1}; {self.clean_data(item)}\n"
        return header, summary, ingredients, nutrients, instructions  # Saved in specific order

    def get_url(self):
        url = simple_dialog.ask_strings("URL Address Dialog", "Enter URL address for recipe: ")
        if url[0] == 'Cancel':
            self.website = ""
        else:
            self.website = url.pop()

    def save_recipe_files(self, f):
        directory = self.check_directory()
        if directory is not None:
            files = list(zip(Import.file_names, f))
            for file_part, data in files:
                path = pathlib.Path(directory, f"{file_part}.txt")
                with open(path, encoding='utf-8', mode="w") as fp:
                    fp.write(data)
            return True

    def start_import(self):
        self.recipe_saved = False
        if not self.website:
            self.get_url()
        if self.website:
            try:
                with request.urlopen(self.website) as response:
                    data = response.read()
            except urllib.error.HTTPError:
                return None, None

            soup = BeautifulSoup(data, "html.parser")
            json_string = soup.find('script', attrs={"type": "application/ld+json"})
            self.data = json.loads(json_string.string)
            self.get_recipe_title()
            if self.data:
                self.json_walk(self.data)
                files = self.get_recipe_files()
                result = self.save_recipe_files(files)
                # print(result)
                if result:
                    self.recipe_saved = True
            else:
                message_dialog.show_message(title="Website Message",
                                            message="Unable to reach the website.")
        return self.recipe_saved, self.recipe_title

    def counter(self):
        self.num = 0
        while True:
            yield self.num
            self.num += 1


if __name__ == "__main__":
    imp = Import()
    imp.start_import()
