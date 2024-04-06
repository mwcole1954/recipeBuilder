import os
import sys
import subprocess
import pathlib
import textwrap
from tkinter import filedialog

import message_dialog

file_names = ("header.txt", "summary.txt", "ingredients.txt", "nutrients.txt", "instructions.txt")
init_dir = pathlib.Path(os.getcwd(), "Recipes")


def write_file(dir_folder, txt_files):
    path = pathlib.Path(dir_folder)
    path = pathlib.Path(path, f'{path.parts[-1]}.txt')
    with open(path, 'w') as fp:
        for item in list(txt_files):
            fp.write(f'{item}\n')


# Read the data from the files of a particular recipe
def create_file_to_print(dir_folder):
    global init_dir
    path = pathlib.Path(dir_folder, 'header.txt')
    if not path.exists():
        result = filedialog.askdirectory(initialdir=pathlib.Path(os.getcwd(), "Recipes"),
                                         title="Select Recipe File To Print")
        print(f'print-select: {result}')
        if pathlib.Path(result).exists():
            init_dir = result
        else:
            return False
    path = pathlib.Path(init_dir)
    if not path.exists():
        return False
    # Collect data
    # HEADER
    header = pathlib.Path(path, 'header.txt')
    with open(header, 'r') as fp:
        data = fp.read().strip()
        data = data.split('\n')
        header_txt = '-' * 5 + "RECIPE" + '-' * 40 + '\n'
        for item in data:
            item = item.split('; ')
        header_txt += f'{item[0].upper()}\n\n'
        if len(item) > 1:
            wrapped = textwrap.fill(item[1].capitalize())
            header_txt += f'{wrapped.strip()}\n'
    # SUMMARY
    summary = pathlib.Path(path, 'summary.txt')
    with open(summary, 'r') as fp:
        data = fp.read().strip()
        data = data.split('\n')
        summary_txt = '-' * 5 + 'SUMMARY' + '-' * 39 + '\n'
        for item in data:
            item = item.split('; ')
            if len(item) == 2 and item[0] != 'name':
                summary_txt += f'  [ ] {item[0].capitalize()}:\t {item[1].capitalize()}\n'
    # INGREDIENTS
    ingredients = pathlib.Path(path, 'ingredients.txt')
    try:
        with open(ingredients, 'r') as fp:
            data = fp.read().strip()
            data = data.split('\n')
    except FileNotFoundError:
        ingredient_txt = ''
    else:
        ingredient_txt = '-' * 5 + 'INGREDIENTS' + '-' * 35 + '\n'
        for n, item in enumerate(data):
            item = item.split('; ')
            if len(item) == 2 and item[0] != 'name':
                if n < 9:
                    ingredient_txt += f'{item[0]} [ ] {item[1].capitalize()}\n'
                else:
                    ingredient_txt += f'{item[0]}[ ] {item[1].capitalize()}\n'

    # INSTRUCTIONS
    instructions = pathlib.Path(path, 'instructions.txt')
    try:
        with open(instructions, 'r') as fp:
            data = fp.read().strip()
            data = data.split('\n')
    except FileNotFoundError:
        instruction_txt = ''
    else:
        instruction_txt = '-' * 5 + 'INSTRUCTIONS' + '-' * 34 + '\n'
        for n, item in enumerate(data):
            item = item.split('; ')
            if len(item) == 2 and item[0] != 'name':
                if n < 9:
                    instruction_txt += f'{item[0]} [ ] ' \
                                       f'{textwrap.fill(item[1].capitalize(), subsequent_indent="      ")}\n'
                else:
                    instruction_txt += f'{item[0]}[ ] ' \
                                       f'{textwrap.fill(item[1].capitalize(), subsequent_indent="      ")}\n'

    # NUTRIENTS
    nutrients = pathlib.Path(path, 'nutrients.txt')
    try:
        with open(nutrients, 'r') as fp:
            data = fp.read().strip()
            data = data.split('\n')
    except FileNotFoundError:
        nutrient_txt = ''
    else:
        nutrient_txt = '-' * 5 + 'NUTRIENTS' + '-' * 37 + '\n'
        for item in data:
            item = item.split('; ')
            if len(item) == 2 and item[0] != 'name':
                nutrient_txt += f'  [ ] {item[0].capitalize()}: {item[1].capitalize()}\n'

        return header_txt, summary_txt, ingredient_txt, instruction_txt, nutrient_txt


def print_recipe(dir_folder):
    path = pathlib.Path(dir_folder)
    path = pathlib.Path(path, f"{path.parts[-1]}.txt")
    if sys.platform == 'win32':
        os.startfile(path, operation="open")
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, path])


def print_file(dir_folder):
    global init_dir
    if dir_folder:
        init_dir = dir_folder
    files = create_file_to_print(init_dir)
    if files:
        write_file(init_dir, files)
        print_recipe(init_dir)
    else:
        message_dialog.show_message("Print File Error", "Unable to print this recipe")


if __name__ == "__main__":
    init_directory = pathlib.Path(os.getcwd(), "Recipes", "My Granola")
    print_file(init_directory)
