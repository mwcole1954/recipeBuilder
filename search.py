import os
import pathlib
import tkinter
from collections import defaultdict

import message_dialog
import search_dialog
import simple_dialog

"""Search either by category or ingredients
"""
class Search:

    def __init__(self):
        self.recipe_title = None
        self.done = False
        self.search_on = None
        self.master = None

    def find_category(self, search_on: str = 'category', search_by: str = ''):
        found_recipes = defaultdict(int)
        # Setting up search criteria
        # if search_by is empty
        if not search_by:
            user_input = simple_dialog.ask_strings("Search By Category", "Enter the criteria for your search: ")
            search_term = [item.lower().strip(', ') for item in user_input[0].split()]
        else:
            search_term = [item.lower().strip(', ') for item in search_by.split()]
        if search_term[0] != 'cancel':
            # The path to the current Recipes folder where all the recipe folders are stored
            folder_path = pathlib.Path(os.getcwd(), "Recipes")
            for recipe in folder_path.iterdir():
                # read the summary.txt file from each folder
                try:
                    with open(pathlib.Path(recipe, 'summary.txt'), encoding='utf-8', mode='r') as fp:
                        for line in fp:
                            if len(line.strip().split('; ')) > 1:
                                lab, val = line.strip().split('; ')
                                val = val.split(', ')
                                if lab.lower() == 'category':
                                    for v in val:
                                        for term in search_term:
                                            if term.lower() in v.lower():
                                                found_recipes[recipe.parts[-1]] += 1
                except FileNotFoundError as msg:
                    pass
                except NotADirectoryError:
                    pass
            if len(found_recipes) > 0:
                txt = f'\t\t\tRecipe Search By Category\n'
                txt += f'\t\t\tTerms: {[item.capitalize() for item in sorted(search_term)]}\n\n'
                for n, recipe in enumerate(found_recipes):
                    # txt += f'{item.name}\n'
                    txt += f'\t\t[  ]{n + 1}:\t{recipe.title()}\n'
                self.show_results(txt)
            else:
                txt = f'No recipes were found related to your criteria: {sorted(search_term)}... '
                message_dialog.show_message("Found Recipes By Category", f'{txt}')

    def get_file(self, event=None):
        if isinstance(event.widget, tkinter.Text):
            event.widget.tag_remove('highlight', 1.0, tkinter.END)
            index = event.widget.index(f"@{event.x},{event.y}")
            start, stop = index.split('.')
            start = int(start)
            stop = int(stop)
            start = start + .0
            stop = start + 1.0
            file = event.widget.get(str(start), str(stop))
            # offsets the char shift
            ndx = file.index(':')
            if file != '' and self.search_on == 'category':
                event.widget.tag_add('highlight', start, stop)
                file = file[ndx + 1:]
                self.done = True
                self.recipe_title = file.strip()
            elif file != '' and self.search_on == 'ingredients':
                ndx2 = file.index(':', ndx + 1)
                event.widget.tag_add('highlight', start, stop)
                file = file[ndx + 1:ndx2]
                self.recipe_title = file.strip()
                self.done = True
            print(file)
            event.widget.tag_config('highlight', background='gray', foreground="white")
            self.quit_app()
            self.destroy_app()

    def quit_app(self):
        self.master.quit()
        self.master.after(100, self.destroy_app)

    def destroy_app(self):
        self.master.destroy()

    def show_results(self, search_results=None):
        if search_results is None:
            search_results = "There were no matches. Try to broaden your search."
        self.master = tkinter.Toplevel()

        self.master.geometry("+300+250")
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)
        vbar = tkinter.Scrollbar(self.master, orient=tkinter.VERTICAL)
        vbar.grid(row=0, column=1, sticky='nsw')
        text = tkinter.Text(self.master, width=100, padx=5, pady=5,
                            wrap=tkinter.WORD, font=('Arial', 12, 'normal'), yscrollcommand=vbar.set)
        text.insert(1.0, search_results)
        text.grid(row=0, column=0, sticky='nsew')
        but_close = tkinter.Button(self.master, text='Close', command=self.master.destroy, anchor='s')
        but_close.grid(row=1, column=0, sticky='s')
        vbar.config(command=text.yview)
        self.master.grab_set()
        self.master.bind("<Button-1>", self.get_file)
        self.master.update()
        self.master.mainloop()


    def find_ingredients(self, search_on: str = 'ingredients', search_by: str = ''):
        found_recipes = defaultdict(set)
        search_terms = [item.strip(',') for item in search_by.split(' ')]
        # Get the list of ingredients
        if not search_by:
            search_terms = simple_dialog.ask_strings("Search By Ingredients", "Enter the ingredients for your "
                                                                              "search: ")

            # If search term not empty, None
            search_terms = search_terms[0].strip().split()
            search_terms = [item.strip(',').lower() for item in search_terms]
        if search_terms != 'Cancel':
            # The path to the current Recipes folder where all the recipe folders are stored
            folder_path = pathlib.Path(os.getcwd(), "Recipes")
            for path in folder_path.iterdir():
                try:
                    with open(pathlib.Path(path, f'{search_on}.txt'), mode='r') as fp:
                        data = fp.read().strip()
                        label_value = data.lower().split('\n')
                except FileNotFoundError as ex:
                    # print(ex)
                    pass
                except NotADirectoryError:
                    pass
                # set up ingredients list to search through
                ingredients = []
                for item in label_value:
                    label_value_line = item.split('; ')
                    if len(label_value_line) > 1:
                        ingredients.append(label_value_line[1].strip().lower())
                # Beginning of search: add search_item found to set for each recipe
                # defaultDict: found_recipes -> key: recipe name : value == set of ingredient matches
                [found_recipes[path.parts[-1]].add(item) for item in search_terms for ing in ingredients if item in ing]
                # print(f"found: {found_recipes}")
            if len(found_recipes) > 0:
                list_order = sorted(found_recipes.items(), key=lambda x: len(x[1]), reverse=True)
                txt = f'\t\t\tIngredient Search Results\n\t\t\tTerms: ' \
                      f'{[item.capitalize() for item in sorted(search_terms)]}\n\n'
                for n, line in enumerate(list_order):
                    txt += f'\t[  ]{n + 1}:\t{line[0].title()}:  {[item.capitalize() for item in sorted(list(line[1]))]}\n'
                self.show_results(txt)
            else:
                message_dialog.show_message("Search By Ingredients", f"Unable to find any recipes that matched the "
                                                                     f"ingredients: "
                                                                     f"{sorted(search_terms)}...")
        else:
            message_dialog.show_message("Search By Ingredients", "Ingredients were not entered for this search. Try again.")

    def start_search(self):
        search_choice = search_dialog.ask_strings("Recipe Search", "Enter the search criteria?")
        if search_choice[0] != 'Cancel':
            search_on, search_by = search_choice
            if search_choice[0].lower() in 'category':
                self.search_on = 'category'
                self.find_category('category', search_by)
            else:
                self.search_on = 'ingredients'
                self.find_ingredients('ingredients', search_by)
        if self.recipe_title != '':
            return self.done, self.recipe_title



if __name__ == "__main__":
    # find_ingredients('ingredients', 'garlic onion paprika')
    find = Search()
    find.find_category("category", '')
    # a = find_category
    # b = find_ingredients
    #
    #
    # def call(func):
    #     func()
    #     print(f"Called func: {func}")
    #     return 'done'

    from random import choice

    # res = call(choice([a, b]))
    # if res == 'done':
    #     exit(0)
