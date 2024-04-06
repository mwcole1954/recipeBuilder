import tkinter

import message_dialog
import simple_dialog
from base_recipe import BaseRecipe
from data import Data
# from scrolled_frame_alt import ScrolledFrame


class Header(tkinter.Frame, BaseRecipe):
    """Panel to hold the header information for the recipe. Inherits from BaseMethods.
        Initiated from main.py and is passed the master widget, label_font and text font.
        Special_list is a conceptual idea but is not used at this point.
        This panel only holds the title and any review information regarding the recipe.
        """

    def __init__(self, master, label_font, font, em_font):
        super().__init__(master)
        # self.inner = None
        # self.sf = None
        self.master = master
        self.last_width = 0
        self.label_font = label_font
        self.font = font
        self.em_font = em_font
        self.recipe_name = 'Untitled Recipe'
        self.data_list = [Data(self.recipe_name, f"Chef's notes...")]
        self.label_list = []
        self.value_list = []
        self.focus = False
        self.save = False  # Will be True if created new data or updated a field
        self.ndx = None
        self.make_panel()

    def __repr__(self):
        return f'Header:{self.data_list} {self.label_list} {self.value_list}'

    def add_return(self, event=None):
        if isinstance(event.widget, tkinter.Text):
            try:
                event.widget.insert('tkinter.INSERT-1c', '\n')
            except Exception:
                pass

    def add_label_value(self):
        # Not adding any labels or values
        # overrides base_recipe class
        message_dialog.show_message("Add Header Label-Value", "You cannot add another label-value to the header.")
        self.focus_set()

    def change_label_text_(self):
        ndx = 0
        new_label_name = simple_dialog.ask_strings(f"Change Header Label Name",
                                                   f"Change label  '{self.data_list[ndx].label}'  to: ",
                                                   default_val=f'{self.data_list[ndx].label}')
        if len(new_label_name) > 0 and new_label_name[0] != 'Cancel':
            self.label_list[ndx].config(text=new_label_name[0])
            self.recipe_name = new_label_name[0]
            self.save = True

        self.update_data_list()
        self.make_panel()
        self.focus_set()
        self.set_focus()

    def del_label_value(self, widget=None):
        # overrides base_recipe class
        # Not deleting any labels or values
        root = self.winfo_toplevel()
        message_dialog.show_message("Remove Header Label-Value", "You cannot remove the label-value to the header.")
        self.focus_set()

    # template and remember to change any title comparisons...
    def get_current_title(self):
        # Update the fields at this time
        self.update_data_list()
        if self.data_list:
            if self.data_list[0].label != "Untitled Recipe":
                return self.data_list[0].label
        return ""

    def reset_on_new(self):
        self.data_list.clear()
        self.data_list.append(Data("Untitled Recipe", "Chef's notes..."))
        self.clear_label_value_list()
        self.reset_flags_vars()

    # GUI
    def make_panel(self):
        self.clear_label_value_list()

        self.config(takefocus=True, padx=5, highlightcolor='blue', highlightthickness=2)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='ew')
        # Use data_list to recreate the label and value lists
        # self.sf = ScrolledFrame(self, scrollbars='vertical', width=600, height=80)
        # self.sf.grid(row=1, column=0, sticky='ew')
        # self.sf.rowconfigure(0, weight=1)
        # self.sf.columnconfigure(0, weight=1)
        # self.inner = self.sf.display_widget(tkinter.Frame, fit_width=True, padx=5)
        # self.inner.columnconfigure(0, weight=1)
        # self.inner.rowconfigure(0, weight=1)
        self.y_scroll = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        self.y_scroll.grid(row=1, column=1, sticky='ns')
        for n, data in enumerate(self.data_list):
            self.label_list.append('')
            self.label_list[n] = tkinter.Label(self, font=self.label_font, anchor='n', padx=5)
            txt = self.data_list[n].label.split()
            txt = [item.capitalize() for item in txt]
            txt = ' '.join(txt)
            self.label_list[n].config(text=txt)
            self.label_list[n].bind("<Button-1>", self.check_b1)
            self.label_list[n].bind("<ButtonRelease-1>", self.check_2b1)  # Change and update the label text
            self.label_list[n].bind("<Enter>", self.on_hover)
            self.label_list[n].bind("<Leave>", self.on_leave_header)
            self.label_list[n].grid(row=0, column=0, sticky='ew')
            self.value_list.append('')
            ht = 5
            self.value_list[n] = tkinter.Text(self, width=100, height=ht, wrap=tkinter.WORD,
                                              font=self.font, takefocus=True, padx=2, undo=True,
                                              yscrollcommand=self.y_scroll.set)
            # ht = math.ceil(len(self.data_list[n].value) / (self.value_list[n]['width']))

            self.value_list[n].config(height=ht)
            t_list = self.data_list[n].value.split('. ')

            txt = '. '.join(f'{item[0].capitalize()}{item[1:]}' for item in t_list)
            txt = txt.replace(' i ', ' I ')
            txt = txt.replace("i'm", "I'm")
            txt = txt.replace(' f ', ' F ')
            txt = txt.replace(' f.', ' F.')
            try:
                start = txt.index("Author:")
                ndx1 = txt.index(' ', start)
                ndx2 = txt.index(' ', ndx1 + 1)
                ndx3 = txt.index(' ', ndx2 + 1)
                change_txt = txt[ndx1:ndx3]
                txt = txt.replace(change_txt, change_txt.title())
                txt = txt.replace('Rdn', 'RDN')
            except ValueError as msg:
                pass
                # print(f"value error: {msg}")
            # lower() here is used for comparison, not syntax
            if self.label_list[n].cget("text").lower() == 'name':
                self.value_list[n].insert('1.0', str(txt))
            else:
                self.value_list[n].insert('1.0', str(txt))
            self.value_list[n].bind("<Button-1>", self.on_panel_click)
            # self.value_list[n].bind("<Return>", self.update_data_list)
            self.value_list[n].bind("<Return>", self.add_return)
            self.value_list[n].grid(row=1, column=0, sticky='ew')
            self.y_scroll.config(command=self.value_list[n].yview)

        # self.sf.bind("<Enter>", lambda _: self.sf.bind_scroll_wheel(self.sf.c))
        # self.sf.bind("<Leave>", self.sf.c.unbind_all("<MouseWheel>"))
        # self.sf.bind("<Button-1>", self.on_panel_click)  # Sets focus to the panel being clicked on
        self.bind("<Button-1>", self.on_panel_click)  # Sets focus to the panel being clicked on
