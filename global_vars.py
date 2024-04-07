import os
import pathlib


class GlobalVars:
    """Class of constants"""

    def __init__(self):
        # List of file names
        self.txt_files_name = ['header', 'summary', 'ingredients', 'nutrients', 'instructions']
        self.label_font = ("Arial", 14, 'bold')
        self.font = ("Arial", 12, 'normal')
        self.em_font = ("Arial", 12, 'bold')
        # Current widget being affected
        self.current_widget = ''
        # Path to the Recipes folder
        self.init_directory = pathlib.Path(os.getcwd(), "Recipes")
        # The current recipe folder; if empty, then working on a new recipe and hasn't been saved
        self.recipe_name = ''
        # List of panel objects
        self.panel_list = list()

    def __repr__(self):
        return GlobalVars.__dict__

    def update_panel_list(self, panel_name):
        self.panel_list.append(panel_name)

    def update_recipe_name(self, recipe_name):
        self.recipe_name = recipe_name

    def update_current_widget(self, widget):
        self.current_widget = widget


if __name__ == "__main__":
    gv = GlobalVars()
    print(gv.__repr__())
