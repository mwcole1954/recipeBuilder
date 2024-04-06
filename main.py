# Built-ins
import os
import pathlib
import platform
import shutil
import sys
import tkinter
from tkinter import filedialog

# Custom scripts
from import_recipes import Import
import message_dialog
from search import Search
import print_recipe
import simple_dialog
import yes_no_dialog
from header import Header
from ingredient import Ingredient
from instruction import Instruction
from nutrition import Nutrition
from summary import Summary

from global_vars import GlobalVars

LABEL_FONT = ("Arial", 14, 'bold')
FONT = ("Arial", 12, 'normal')
EM_FONT = ("Arial", 12, 'bold')
BUTTON_FONT = ("Arial", 10, 'bold')

# Initialize global variables
globalVars = GlobalVars()


def about_program(*_):
    message_dialog.show_message("Welcome to Recipe Builder",
                                "This is version 4.4.\nThanks for trying it.\nWritten in Python 3.11. If you have any "
                                "problems\n"
                                "you can contact\nMichael at 'mwcole1954@gmail.com'", text_height=5)


def add(event=None):
    counter = 0
    # Check for a panel that has is current_widget
    for item in globalVars.panel_list:
        if item.focus:
            item.focus_force()
            w = root.focus_get()
            w.focus_set()
            item.add_label_value()
            break
        counter += 1
    if counter == len(globalVars.panel_list):
        # If none have focus, then ask user for panel name to add data
        # get the panel to add label/value
        choice = simple_dialog.ask_strings("Select The Panel", "Which panel do you want to add information: ")
        if choice and choice[0] != 'Cancel':
            panel = choice[0].lower()
            for item in globalVars.panel_list:
                if str(item) != 'header':
                    if panel in str(item):
                        item.focus = True
                        item.add_label_value()
                        item.focus_force()
                        w = root.focus_get()
                        w.focus_set()
                        break


# Check where current focus is based on the widgets
def check_all_widgets(event):
    # Updates the current_widget flag in the global variables
    globalVars.current_widget = str(event.widget)
    event.widget.focus_set()
    # root.tk_focusNext().focus()
    # return 'break'


# Check all panel.save
def check_all_flags():
    """Loops through panels; looking for the need to save any changes"""
    for panel in globalVars.panel_list:
        if panel.save:
            return True


def close(*_):
    # Close first checks that there are no save flags that are True
    # If there are, the user is prompted to SAVE, YES or NO
    # Then the program closes
    if check_all_flags():
        if want_to_save():
            if globalVars.recipe_name == "":
                if header.get_current_title() == "":
                    message_dialog.show_message("Recipe Name Message", "Need to create a recipe name")
                    return
                elif header.get_current_title() != "":
                    save_new_recipe_name()
            else:
                if globalVars.recipe_name.strip().lower() != header.get_current_title().strip().lower():
                    if header.get_current_title() != "":
                        if not rename_recipe_folder(header.get_current_title()):
                            return
            final_save()
    root.destroy()
    sys.exit()


def delete(*_):
    # Removes the selected item in the panel
    panel = ''
    counter = 0
    # Check for a panel that is current_widget
    for item in globalVars.panel_list:
        if item.focus:
            item.del_label_value()
            break
        counter += 1
    if counter == len(globalVars.panel_list):
        choice = simple_dialog.ask_strings("Select The Panel",
                                           "Which panel do you want to remove information: ")
        if len(choice) == 1:
            panel = choice[0]
        if panel != 'Cancel' and len(panel.strip()) > 0:
            for item in globalVars.panel_list:
                if panel in str(item):
                    item.del_label_value()
                    break
    reset_current_widget()


def do_reset_save():
    for panel in globalVars.panel_list:
        panel.reset_save()


def do_reset_new():
    """This occurs when any file that needs to be saved has been saved
    and then the program sets up a blank recipe template with all flags
    and recipe_name reset to "False" and ''.
    :return: None
    """
    for panel in globalVars.panel_list:
        panel.reset_on_new()
        panel.make_panel()
        panel.reset_save()
    reset_recipe_name()
    reset_current_widget()


def do_search(*_):
    # Get user criteria; by category which is found in the summary.txt panel or by ingredients
    # Returns a list with two responses: search option (search_on) and search criteria (search_by)
    search = Search()
    search.done, search.recipe_title = search.start_search()
    done = search.done;
    file = search.recipe_title
    if file:
        open_file('open-import', file)


def do_update(*_):
    # Updates the data_list of each panel; run before saving
    for panel in globalVars.panel_list:
        panel.update_data_list()


def enter(event):
    if isinstance(event.widget, tkinter.Button):
        if event.widget['state'] != 'normal':
            # print(f"enter widget: {event.widget} {event} {event.widget['state']}")
            pass
        else:
            # event.widget['bg'] = 'black'
            # event.widget['fg'] = 'white'
            event.widget['font'] = BUTTON_FONT


def final_save(*_):
    # This is done once all flag checks are completed looking for need to save, need to change file name,
    # need to create a file name
    pn = ''
    if globalVars.recipe_name.strip() == '' and len(header.get_current_title().strip()) > 0:
        save_new_recipe_name()
    elif globalVars.recipe_name.strip() != header.get_current_title().strip():
        if pathlib.Path(globalVars.init_directory, globalVars.recipe_name).exists():
            try:
                os.rename(pathlib.Path(globalVars.init_directory, globalVars.recipe_name), pathlib.Path(
                    globalVars.init_directory, header.get_current_title().strip()))
                globalVars.recipe_name = header.get_current_title().strip()
            except FileExistsError:
                message_dialog.show_message("File Rename Error", "Cannot rename recipe file because another recipe "
                                                                 "file exists with the new name.")
                return
    if globalVars.recipe_name:
        for num, panel in enumerate(globalVars.panel_list):
            if str(panel).split("!")[-1][:3] == globalVars.txt_files_name[num][:3]:
                pn = globalVars.txt_files_name[num]
            panel.save_file(globalVars.init_directory, globalVars.recipe_name, pn)
            panel.reset_flags_vars()
        message_dialog.show_message("Save File Message", f"The files for {globalVars.recipe_name} have been saved ")
        return True
    # message_dialog.show_message("Save File Message", "The files were not saved because there was no recipe title...")
    header.change_label_text_()


def help_file(*_):
    with open('help_files.txt', 'r') as fp:
        data = fp.read()
    top = tkinter.Toplevel(pady=5)
    top.title("Recipe Builder Help")
    top.geometry("1000x700+300+25")
    top.columnconfigure(0, weight=1)
    top.rowconfigure(0, weight=1)
    vsb = tkinter.Scrollbar(top, orient=tkinter.VERTICAL)
    vsb.grid(row=0, column=1, sticky='ns')
    note = tkinter.Text(top, width=80, height=50, font=FONT, padx=50, pady=10, wrap='word',
                        yscrollcommand=vsb.set)
    note.grid(row=0, column=0, sticky='nsew')
    but = tkinter.Button(top, text="Close", width=10, command=top.destroy, anchor='s')
    but.grid(row=1, column=0, sticky='s')
    vsb.config(command=note.yview)
    note.insert("1.0", data)
    note.tag_add("center", 1.0, 4.0)
    note.tag_add("left", 4.0, tkinter.END)
    note.tag_config("center", justify=tkinter.CENTER)
    note.tag_config("left", justify=tkinter.LEFT)
    note.config(state="disabled")
    top.grab_set()


# Button Leave with cursor
def leave(event):
    if isinstance(event.widget, tkinter.Button):
        if event.widget['state'] != 'normal':
            # print(f"leaving widget: {event.widget} {event} {event.widget['state']}")
            pass
        else:
            # event.widget['bg'] = 'white'
            # event.widget['fg'] = 'black'
            event.widget['font'] = BUTTON_FONT


def new(*_):
    # print(*_)
    # Check if there is information that needs to be saved prior to setting up a new, empty template
    if check_all_flags():
        if want_to_save():
            if globalVars.recipe_name == "":
                if header.get_current_title() == "":
                    message_dialog.show_message("Recipe Name Message", "Need to create a recipe name")
                    return
                elif header.get_current_title() != "":
                    save_new_recipe_name()
            else:
                if globalVars.recipe_name.strip().lower() != header.get_current_title().strip().lower():
                    if header.get_current_title() != "":
                        rename_recipe_folder(header.get_current_title())
            final_save()
    do_reset_new()


def open_file(*args):
    # Does the Recipe folder exist?
    print(os.getcwd())
    if not pathlib.Path(os.getcwd(), 'Recipes').exists():
        pathlib.Path.mkdir(pathlib.Path(os.getcwd(), 'Recipes'))
    # Do you have any changes to save before opening another file?
    if check_all_flags():
        if want_to_save():
            if globalVars.recipe_name == "":
                if header.get_current_title() == "":
                    message_dialog.show_message("Recipe Name Message", "Need to create a recipe name")
                    return
                elif header.get_current_title() != "":
                    save_new_recipe_name()
            else:
                if globalVars.recipe_name.strip().lower() != header.get_current_title().strip().lower():
                    if header.get_current_title() != "":
                        if not rename_recipe_folder(header.get_current_title()):
                            return
            final_save()
    # then show the imported recipe
    if len(args) > 1:
        o, r = args
        if o == 'open-import':
            for num, panel in enumerate(globalVars.panel_list):
                globalVars.recipe_name = r
                panel.read_file(globalVars.init_directory, globalVars.recipe_name, globalVars.txt_files_name[num])
                panel.update_data_list()
            do_reset_save()
            return
    # then show open dialog box
    dir_chosen = filedialog.askdirectory(initialdir=globalVars.init_directory, mustexist=True,
                                         title="Select Your Recipe...")
    if dir_chosen and dir_chosen != 'Cancel':
        globalVars.recipe_name = dir_chosen.split('/')[-1]
        # Required functions and order to set up flags after reading a recipe file globalVars.
        for num, panel in enumerate(globalVars.panel_list):
            if str(panel).split("!")[-1][:3] == globalVars.txt_files_name[num][:3]:
                # pn = globalVars.txt_files_name[num]
                panel.reset_on_new()  # Clears all lists
                # print(f"directory: {globalVars.init_directory}, recipe_name: {globalVars.recipe_name}, pn: {pn}")
                panel.read_file(globalVars.init_directory, globalVars.recipe_name, globalVars.txt_files_name[num])
                panel.update_data_list()  # update sets save to True
    do_reset_save()


def printing_recipe(*_):
    # If a recipe is open in the application
    if globalVars.init_directory and globalVars.recipe_name:
        path = pathlib.Path(globalVars.init_directory, globalVars.recipe_name)
        print_recipe.print_file(path)
    else:
        message_dialog.show_message("Print Recipe File",
                                    "No recipe is open. Open the recipe file that you want to print.")


def remove_trash(*_):
    remove = filedialog.askdirectory(initialdir=globalVars.init_directory, mustexist=True, title="Select the recipe "
                                                                                                 "to remove "
                                                                                                 "to the trash: ")
    # the initial directory is part of new directory
    if remove:
        path_name = pathlib.Path(globalVars.init_directory, remove)
        try:
            shutil.rmtree(path_name)
        except OSError as e:
            message_dialog.show_message("Delete File Error Message", "Error: %s - %s." % (e.filename, e.strerror))
        else:
            message_dialog.show_message("Delete Recipe File",
                                        f"The recipe: '{pathlib.Path(remove).parts[-1]}' has been "
                                        f"deleted")
    # else:
    #     message_dialog.show_message("Delete Recipe File", "A recipe file was not selected...")


# rename recipe folder, but if folder does not exist, create new folder
def rename_recipe_folder(new_fn: str):
    """Renames a recipe folder when the user changes the name of the recipe
    :param new_fn: this is the new recipe name
    :return: None
    """
    path = pathlib.Path(globalVars.init_directory, globalVars.recipe_name)
    if path.exists():
        fn = new_fn.strip()
        try:
            os.rename(path, pathlib.Path(globalVars.init_directory, fn))
        except FileExistsError:
            message_dialog.show_message("Rename Recipe Message",
                                        "That recipe name already exists. Change the name and try again.")
            return False
        else:
            globalVars.recipe_name = fn
            return True


def reset_recipe_name():
    globalVars.recipe_name = ''


def reset_current_widget():
    globalVars.current_widget = ''


# create or update recipe_name
def save_new_recipe_name():
    """Checks to see if the new recipe name is available to create the new recipe folder.
    If it is, then it calls create_recipe_folder. Otherwise, it prompts the user to name the
    recipe."""
    # recipe_name was ''; set it to header.txt.get_current_title
    # create the new recipe folder
    new_path = pathlib.Path(os.getcwd(), "Recipes", header.get_current_title())
    try:
        os.mkdir(new_path)
    except FileExistsError:
        message_dialog.show_message("Create Recipe Name Message",
                                    "This recipe name already exists. Please change the recipe "
                                    "name and try again.")
        return False
    else:
        globalVars.recipe_name = header.get_current_title()
        return True


def save(*_):
    # Is there a recipe folder
    # Check need to create or rename recipe title
    if check_all_flags():
        if want_to_save():
            if globalVars.recipe_name == "":
                if header.get_current_title() == "":
                    message_dialog.show_message("Recipe Name Message", "Need to create a recipe name")
                    return
                elif header.get_current_title() != "":
                    save_new_recipe_name()
            else:
                if globalVars.recipe_name.strip().lower() != header.get_current_title().strip().lower():
                    if header.get_current_title() != "":
                        if not rename_recipe_folder(header.get_current_title()):
                            return
            final_save()
    else:
        message_dialog.show_message("Save Dialog", "No changes have been made. Save is not necessary.")


def scrape(*_):
    # Get the URL for the scraping and clean up
    get_recipe = Import()
    saved, recipe = get_recipe.start_import()
    if saved:
        open_file('open-import', recipe)
    else:
        message_dialog.show_message("Import Dialog", "Unable to save the imported recipe.")


def want_to_save():
    response = yes_no_dialog.show_yes_no("Remind To Save", "You have made some changes? Do you want to save them?")
    if response:
        return True
    return False


# GUI -----------------------------------
root = tkinter.Tk()
# Turn off the tearOff option
root.option_add('*tearOff', False)
root.title("Recipe Builder")
root.geometry("+250+25")
root.config()
root.minsize(300, 300)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)

header_frame = tkinter.Frame(root, padx=25)
header_frame.rowconfigure(0, weight=1)
header_frame.rowconfigure(1, weight=1)
header_frame.columnconfigure(0, weight=1)
header_frame.grid(row=0, column=0, sticky='ew')
top_frame = tkinter.Frame(root)
top_frame.columnconfigure(0, weight=1)
top_frame.columnconfigure(1, weight=1)
top_frame.columnconfigure(2, weight=1)
top_frame.grid(row=1, column=0, sticky='ew')
bottom_frame = tkinter.Frame(root)
bottom_frame.columnconfigure(0, weight=1)
bottom_frame.grid(row=2, column=0, sticky='ew')

# PANELS
header = Header(header_frame, LABEL_FONT, FONT, EM_FONT)
summary = Summary(top_frame, LABEL_FONT,
                  FONT, EM_FONT, special_list=['name', 'active'])
ingredient = Ingredient(top_frame, LABEL_FONT, FONT, EM_FONT)
nutrition = Nutrition(top_frame, LABEL_FONT, FONT, EM_FONT)
instruction = Instruction(bottom_frame, LABEL_FONT, FONT, EM_FONT)
# Populate panel_list
globalVars.panel_list.extend([header, summary, ingredient, nutrition, instruction])

# MENUBAR ITEMS
menubar = tkinter.Menu(root)
root.config(menu=menubar)
menu_file = tkinter.Menu(menubar)
menu_edit = tkinter.Menu(menubar)
menu_tool = tkinter.Menu(menubar)
menu_help = tkinter.Menu(menubar)
menubar.add_cascade(menu=menu_file, label="File")
menubar.add_cascade(menu=menu_edit, label='Edit')
menubar.add_cascade(menu=menu_tool, label='Tool')
menubar.add_cascade(menu=menu_help, label='Help')

# menu_file
if platform.system() == 'Windows':
    menu_file.add_command(label='New', command=new)
    menu_file.entryconfig('New', accelerator='Ctrl+n')
    menu_file.add_command(label='Open', command=open_file)
    menu_file.entryconfig('Open', accelerator='Ctrl+o')
    menu_file.add_separator()
    menu_file.add_command(label='Save', command=final_save)
    menu_file.entryconfig('Save', accelerator='Ctrl+s')
    menu_file.add_separator()
    menu_file.add_command(label='Print', command=printing_recipe)
    menu_file.entryconfig('Print', accelerator='Ctrl+p')
    menu_file.add_separator()
    menu_file.add_command(label='Exit', command=close)
    menu_file.entryconfig('Exit', accelerator='Ctrl+q')
    # menu_edit
    menu_edit.add_command(label='Add', command=add)
    menu_edit.entryconfig('Add', accelerator='Ctrl+a')
    menu_edit.add_command(label='Remove', command=delete)
    menu_edit.entryconfig('Remove', accelerator='Ctrl+r')
    menu_edit.add_separator()
    menu_edit.add_command(label='Update', command=do_update)
    menu_edit.entryconfig('Update', accelerator='Ctrl+u')
    menu_edit.add_separator()
    menu_edit.add_command(label='Delete', command=remove_trash)
    menu_edit.entryconfig('Delete', accelerator='Ctrl+d')
    # menu_tool
    menu_tool.add_command(label='Search', command=do_search)
    menu_tool.entryconfig('Search', accelerator='Ctrl+Alt+s')
    menu_tool.add_command(label='Import', command=scrape)
    menu_tool.entryconfig('Import', accelerator='Ctrl+I')
    # menu_help
    menu_help.add_command(label='Help', command=help_file)
    menu_help.entryconfig('Help', accelerator='Ctrl+h')
    menu_help.add_command(label="About", command=about_program)
    menu_help.entryconfig('About', accelerator='Ctrl+Alt+a')

elif platform.system() == "Darwin":
    menu_file.add_command(label='New', command=new)
    menu_file.entryconfig('New', accelerator='Command+n')
    menu_file.add_command(label='Open', command=open_file)
    menu_file.entryconfig('Open', accelerator='Command+o')
    menu_file.add_separator()
    menu_file.add_command(label='Save', command=final_save)
    menu_file.entryconfig('Save', accelerator='Command+s')
    menu_file.add_separator()
    menu_file.add_command(label='Print', command=printing_recipe)
    menu_file.entryconfig('Print', accelerator='Command+p')
    menu_file.add_separator()
    menu_file.add_command(label='Exit', command=close)
    menu_file.entryconfig('Exit', accelerator='Command+q')
    # menu_edit
    menu_edit.add_command(label='Add', command=add)
    menu_edit.entryconfig('Add', accelerator='Command+a')
    menu_edit.add_command(label='Remove', command=delete)
    menu_edit.entryconfig('Remove', accelerator='Command+r')
    menu_edit.add_separator()
    menu_edit.add_command(label='Update', command=do_update)
    menu_edit.entryconfig('Update', accelerator='Command+u')
    menu_edit.add_separator()
    menu_edit.add_command(label='Delete', command=remove_trash)
    menu_edit.entryconfig('Delete', accelerator='Command+d')
    # menu_tool
    menu_tool.add_command(label='Search', command=do_search)
    menu_tool.entryconfig('Search', accelerator='Command+Alt+s')
    menu_tool.add_command(label='Import', command=scrape)
    menu_tool.entryconfig('Import', accelerator='Command+i')
    # menu_help
    menu_help.add_command(label='Help', command=help_file)
    menu_help.entryconfig('Help', accelerator='Command+h')
    menu_help.add_command(label="About", command=about_program)
    menu_help.entryconfig('About', accelerator='Command+Alt+a')

# BINDS
if platform.system() == 'Windows':
    root.bind("<Control - n>", new)
    root.bind("<Control - o>", open_file)
    root.bind("<Control - a>", add)
    root.bind("<Control - r>", delete)
    root.bind("<Control - s>", final_save)
    root.bind("<Control - q>", close)
    root.bind("<Control - i>", scrape)
    root.bind("<Control - p>", printing_recipe)
    root.bind("<Control - h>", help_file)
    root.bind("<Control - d>", remove_trash)
    root.bind("<Control -u>", do_update)
    root.bind("<Control - Alt - s>", do_search)
    root.bind("<Control - Alt - a>", about_program)
    root.bind("<Button-1>", check_all_widgets)

elif platform.system() == 'Darwin':
    root.bind("<Command - n>", new)
    root.bind("<Command - o>", open_file)
    root.bind("<Command - a>", add)
    root.bind("<Command - r>", delete)
    root.bind("<Command - s>", final_save)
    root.bind("<Command - q>", close)
    root.bind("<Command - i>", scrape)
    root.bind("<Command - p>", printing_recipe)
    root.bind("<Command - h>", help_file)
    root.bind("<Command - d>", remove_trash)
    root.bind("<Command - u>", do_update)
    root.bind("<Command - Alt - s>", do_search)
    root.bind("<Command - Alt - a>", about_program)
    root.bind("<Button-1>", check_all_widgets)

do_update()
do_reset_save()
root.update()

root.mainloop()
