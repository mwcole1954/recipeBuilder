import os
import pathlib


class GlobalVars:
    """Class of constants"""

    # LABEL_FONT = ("Arial", 14, 'bold')
    # FONT = ("Arial", 12, 'normal')
    # EM_FONT = ("Arial", 12, 'bold')

    current_widget = ''

    # Path to the Recipes folder
    init_directory = pathlib.Path(os.getcwd(), "Recipes")
    # The current recipe folder; if empty, then working on a new recipe and hasn't been saved
    recipe_name = ''
    # List of panel objects
    panel_list = []
    # List of file names
    txt_files_name = ['header', 'summary', 'ingredients', 'nutrients', 'instructions']
