import os
import pathlib
import tkinter

from abc import ABC, abstractmethod
from drag_drop import DragDrop

import global_vars
import header
import message_dialog
import simple_dialog
from data import Data
from yes_no_dialog import show_yes_no


class BaseRecipe(DragDrop, ABC):
    """This is a base class that maintains much of the functionality of the panels
    but allows more centralization of code. It is inherited by all the panel classes.
    """

    clean = {
        '�': '?',
        '&amp;': '&',
        ';': ',',
        '   ': '',
        'content': '',
        'fat': ' fat',
        ' fat': ' fat',
        '  fat': ' fat',
        '   fat': ' fat',
        'preptime': 'prep time',
        'prepTime': 'prep time',
        'cooktime': 'cook time',
        'totaltime': 'total time',
        'recipeyield': 'yield',
        'recipe yield': 'yield',
        'recipeYield': 'yield',
    }

    def __init__(self):
        super().__init__()

    def add_label_value(self):
        panel_name = self.__str__().split('.!')[-1]
        if panel_name in ('summary', 'nutrition'):
            data = simple_dialog.ask_strings(f"Enter {panel_name.capitalize()} Data", f"Enter the name for the label: ",
                                             "Enter the information: ")
            if data[0] != 'Cancel' and data[0] != '' and data[1] != '':
                self.data_list.append(Data(data[0], data[1]))
                self.save = True
        else:
            tmp_val = len(self.label_list) + 1
            data = simple_dialog.ask_strings(f"Enter {panel_name.capitalize()} Data",
                                             f"Enter the position of the ingredient: ",
                                             f"Enter the {panel_name.lower()} information: ", default_val=tmp_val)
            if data[0] != 'Cancel' and data[0] != '' and data[1] != '':
                if str(data[0]).isnumeric():
                    self.data_list.insert(int(data[0]) - 1, Data(data[0], data[1]))
                    self.save = True
                else:
                    message_dialog.show_message(title="Data Entry Error",
                                                message="A number is required for the position.")
                    return None
        self.make_panel()
        self.update_data_list()
        self.master.focus_set()
        self.set_focus()
        self.get_widget_list()

    def change_label_text(self, event):
        """Brings up a dialog to change the name of the label in Header, Summary or Nutrition panels"""
        # Change cursor to denote changing the text
        # self.on_hover(event)
        if isinstance(event.widget, tkinter.Label):
            if event.widget in self.label_list:
                ndx = self.label_list.index(event.widget)
                panel_name = [item for item in ('header', 'summary', 'nutrition') if item in self.__str__()]
                new_label_name = simple_dialog.ask_strings(f"Change {panel_name[0].capitalize()} Label Name",
                                                           f"Change label  '{self.data_list[ndx].label}'  to: ",
                                                           default_val=f'{self.data_list[ndx].label}')
                if len(new_label_name) > 0 and new_label_name[0] != 'Cancel':
                    self.label_list[ndx].config(text=new_label_name[0])
                    self.save = True

            self.update_data_list()
            self.make_panel()
            self.set_focus()



    def check_b1(self, event):
        self.on_panel_click(event)
        """Binding for B-1, if B-1 is held down and there is MOTION, it directs to drag_drop.py"""
        if not isinstance(self, header.Header):
            if isinstance(event.widget, tkinter.Text) or isinstance(event.widget, tkinter.Label):
                event.widget.bind("<B1-Motion>", lambda e: self.on_click(event))

    def check_2b1(self, event):
        """Changes the cursor when editing the labels"""
        if isinstance(event.widget, tkinter.Label):
            event.widget.config(cursor='exchange')
            self.change_label_text(event)

    def clean_data(self, l_list, v_list):
        # Clean the label information. Can be edited via the clean dictionary.
        for n in range(len(l_list)):
            l_list[n] = l_list[n]
            l_list[n] = l_list[n].strip()
            for key in self.clean:
                l_list[n] = l_list[n].replace(key, self.clean[key])
        for n in range(len(v_list)):
            v_list[n] = v_list[n]
            v_list[n] = v_list[n].strip()
            for key in self.clean:
                v_list[n] = v_list[n].replace(key, self.clean[key])

        if len(l_list) == 1 and l_list[0] == '' or len(v_list) == 1 and v_list[0] == '':
            l_list.clear()
            v_list.clear()
        return l_list, v_list

    def clear_label_value_list(self):
        self.label_list.clear()
        self.value_list.clear()

    def clear_data_list(self):
        self.data_list.clear()


    def del_label_value(self):
        panel_name = self.__str__().split('.!')[-1]
        # If the label list for the panel is not empty
        if len(self.label_list) > 0:
            if panel_name in ('summary', 'nutrition', 'ingredient', 'instruction'):
                try:
                    label_choice = show_yes_no(f"Remove {panel_name.capitalize()} Data",
                                               f"Do you want to remove the label: '"
                                               f"{self.label_list[self.ndx].cget('text')}'? ")
                except TypeError:
                    message_dialog.show_message(f"{panel_name.capitalize()} Remove Error\n\n",
                                                "You need to select the field that you want to remove.")
                else:
                    if label_choice:
                        self.data_list.pop(self.ndx)
                        self.save = True
                        self.ndx = None  # Reset self.ndx after the data_list is popped
                        self.make_panel()
                        self.update_data_list()
                        self.set_focus()
                        self.get_widget_list()
        else:
            message_dialog.show_message(f"Remove {panel_name} Data", "Nothing to remove here.")

    def get_widget_list(self):
        root = self.master.winfo_toplevel()
        if len(self.data_list) == 0 or 'head' in self.__str__():
            root.nametowidget('.!menu.!menu2').entryconfig("Remove", state='disabled')
        else:
            root.nametowidget('.!menu.!menu2').entryconfig("Remove", state='normal')
        if 'head' in self.__str__():
            root.nametowidget('.!menu.!menu2').entryconfig("Add", state='disabled')
        else:
            root.nametowidget('.!menu.!menu2').entryconfig("Add", state='normal')


    @abstractmethod
    def make_panel(self):
        raise NotImplementedError

    def on_hover(self, event):
        # self.set_panel_focus(event)
        if isinstance(event.widget, tkinter.Label) or isinstance(event.widget, tkinter.Text):
            event.widget.config(fg='gray')
            # event.widget.config(cursor='exchange')

    def on_leave(self, event):
        if isinstance(event.widget, tkinter.Label):
            event.widget.config(fg='black', font=self.em_font)
        elif isinstance(event.widget, tkinter.Text):
            event.widget.config(fg='black', font=self.font)

    def on_leave_header(self, event):
        if isinstance(event.widget, tkinter.Label):
            event.widget.config(fg='black', font=self.label_font)

    def on_panel_click(self, event):
        self.unset_panel_focus()
        self.set_panel_focus(event)
        self.get_widget_list()

    # Used when reading a new recipe file; reset variables and flags
    def reset_flags_vars(self):
        self.reset_save()

    def reset_on_new(self):
        self.data_list.clear()
        self.clear_label_value_list()
        self.reset_flags_vars()

    def reset_save(self):
        self.save = False

    def read_file(self, directory, fn, pn):
        # fn: recipe name; pn: panel name
        # Clear all data list
        self.reset_on_new()
        # Store the current working directory
        self.recipe_name = fn.lower()
        # Get the file data
        the_file = pathlib.Path(directory, fn, f'{pn}.txt')
        try:
            with open(the_file, encoding='utf-8', mode='r') as fp:
                data = fp.read()
                if pn == 'header':
                    label_value_list = data.strip().split('; ')
                else:
                    label_value_list = data.strip().split('\n')
        except FileNotFoundError as msg:
            return [None], [None]
        else:
            label_list = []
            value_list = []
            if pn == 'header':
                label_list.append(label_value_list[0])
                value_list.append(label_value_list[1])

            for item in label_value_list:
                label_value_line = item.strip().split('; ')
                if len(label_value_line) == 2:
                    if label_value_line[0].lower() == "the recipe title":
                        label_value_line[0] = "Untitled Recipe"
                    label_list.append(label_value_line[0])
                    value_list.append(label_value_line[1])
            l_list, v_list = self.clean_data(label_list, value_list)

        if l_list and v_list:
            self.data_list = [Data(*item) for item in zip(l_list, v_list)]
        self.make_panel()

    def save_file(self, directory, fn, pn):
        # fn: recipe folder name; pn: panel name
        label_value = ''

        for data in self.data_list:
            label_value += f'{str(data.label)}; {str(data.value)}\n'
            label_value.rstrip().rstrip('; ')

        file_path = pathlib.Path(directory, fn)
        file_name = f'{pn}.txt'
        if file_path and file_name and label_value:
            fn = pathlib.Path(file_path, f'{file_name}')
            try:
                with open(fn, encoding='utf-8', mode='w') as fp:
                    fp.writelines(label_value)
            except FileExistsError:
                pass
            except FileNotFoundError:
                # Create the file_path + file_name if possible
                os.mkdir(pathlib.Path(file_path, file_name))
            return True
        return False

    def set_focus(self):
        self.focus = True
        self.focus_set()


    def set_panel_focus(self, event):
        # self.unset_panel_focus()
        self.focus = True
        event.widget.focus_set()
        self.set_focus()
        if isinstance(event.widget, tkinter.Text):
            if event.widget.winfo_name()[-1].isnumeric():
                self.ndx = int(event.widget.winfo_name()[-1]) - 1
            else:
                self.ndx = 0

    def unset_panel_focus(self):
        for panel in global_vars.GlobalVars.panel_list:
            panel.focus = False
            panel.ndx = None

    def update_data_list(self, *args):
        if 'summary' in self.__class__.__name__.lower() or 'nutrition' in self.__class__.__name__.lower() or \
                'header' in self.__class__.__name__.lower():
            # Collect the data in the fields and the data list
            for n, data in enumerate(self.data_list):
                if len(self.label_list) > 0 and len(self.value_list) > 0:
                    if data.label.strip() != self.label_list[n].cget("text").strip() or data.value.strip() != \
                            self.value_list[n].get(1.0, tkinter.END).strip():
                        data.label = self.label_list[n].cget("text").strip()
                        data.value = self.value_list[n].get(1.0, tkinter.END).strip()
                        self.save = True
        elif 'ingredient' in self.__class__.__name__.lower() or 'instruction' in self.__class__.__name__.lower():
            for n, data in enumerate(self.data_list):
                # if data.label.strip() != self.label_list[n].cget("text").strip() or data.value.strip() != \
                #         self.value_list[n].get(1.0, tkinter.END).strip():
                # Allows inserting, etc of items in the list and corrects the count
                data.label = str(n + 1)
                data.value = self.value_list[n].get(1.0, tkinter.END).strip()
                self.save = True
        self.make_panel()
