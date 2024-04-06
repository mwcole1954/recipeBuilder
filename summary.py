import math
import tkinter

from scrolled_frame_alt import ScrolledFrame
from base_recipe import BaseRecipe
from drag_drop import DragDrop


class Summary(tkinter.LabelFrame, BaseRecipe, DragDrop):
    """Panel to hold the summary information for the recipe. Inherits from BaseMethods.
        Initiated from main.py and is passed the master widget, label_font and text font.
        Special_list allows adding title() for certain values by adding a list of label names."""

    def __init__(self, master, label_font, font, em_font, *, special_list=None):
        super().__init__(master)

        self.sf = None
        self.inner_frame = None
        self.label_font = label_font
        self.font = font
        self.em_font = em_font
        self.config(text="Summary", font=self.label_font)
        self.save = False  # Will be True if created new data or updated a field
        self.master = master
        self.data_list = []
        self.label_list = []
        self.value_list = []
        self.panel_empty = True
        self.focus = False
        self.ndx = None
        self.recipe_name = ''
        self.special_list = ['level', 'category', 'name', 'cuisine']
        if special_list:
            self.special_list.extend([item.lower() for item in special_list if item not in
                                      self.special_list])

    def __repr__(self):
        return f'Summary: {self.data_list} {self.label_list} {self.value_list}'

    # GUI
    def make_panel(self, *args):
        self.clear_label_value_list()
        self.config(takefocus=True, highlightcolor="blue", highlightthickness=2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='nsew')
        # Scroll frame to put the label and text fields into
        self.sf = ScrolledFrame(self, scrollbars="vertical")
        self.sf.config(takefocus=True)
        self.sf.columnconfigure(0, weight=1)
        self.sf.grid(row=0, column=0, sticky='nsew')
        self.inner_frame = self.sf.display_widget(tkinter.Frame, fit_width=True, padx=2)
        self.inner_frame.columnconfigure(1, weight=1)
        # Use data_list to recreate the label and value lists
        for n, data in enumerate(self.data_list):
            self.rowconfigure(0, weight=1)
            self.inner_frame.rowconfigure(n, weight=1)
            self.label_list.append('')
            self.label_list[n] = tkinter.Label(self.inner_frame, font=self.em_font,
                                               takefocus=True, anchor='e', width=8, height=1, padx=2)
            self.label_list[n].config(text=self.data_list[n].label.title())
            # self.label_list[n].bind("<Button-3>", self.on_click)            # Move label
            # self.label_list[n].bind("<Button-1>", self.change_label_text)   # EDIT label
            self.label_list[n].bind("<Button-1>", self.check_b1)
            self.label_list[n].bind("<ButtonRelease-1>", self.check_2b1)
            self.label_list[n].bind("<Enter>", self.on_hover)  # FOCUS IN label  Tried need to retest
            self.label_list[n].bind("<Leave>", self.on_leave)
            self.label_list[n].bind("<Return>", self.update_data_list)
            self.label_list[n].grid(row=n, column=0, sticky='ew')

            self.value_list.append('')
            ht = 1
            self.value_list[n] = tkinter.Text(self.inner_frame, width=25, height=ht, wrap=tkinter.WORD, font=self.font,
                                              padx=2, undo=True, highlightcolor='black', highlightthickness=1,
                                              takefocus=True, maxundo=-1)
            ht = math.ceil(len(self.data_list[n].value) / (self.value_list[n]['width'] + 11))
            self.value_list[n].config(height=ht)
            # clean up some text before being written; TODO: centralize this
            self.data_list[n].value = self.data_list[n].value.replace('Pt', '')
            if self.label_list[n].cget("text").lower() in self.special_list:
                self.value_list[n].insert(1.0, self.data_list[n].value.title())
            else:
                self.value_list[n].insert(1.0, self.data_list[n].value.capitalize())
            self.value_list[n].bind("<Button-1>", self.check_b1)
            self.value_list[n].bind("<Double-Button-1>", self.check_2b1)
            # self.value_list[n].bind("<Button-1>", self.on_panel_click)  # Set focus to the panel being clicked
            self.value_list[n].bind("<Enter>", self.on_hover)
            self.value_list[n].bind("<Leave>", self.on_leave)
            # self.value_list[n].bind("<Button-3>", self.on_click)
            self.value_list[n].bind("<Return>", self.update_data_list)
            self.value_list[n].grid(row=n, column=1, sticky='ew')
        self.sf.bind("<Enter>", lambda _: self.sf.bind_scroll_wheel(self.sf.c))
        self.sf.bind("<Leave>", self.sf.c.unbind_all("<MouseWheel>"))
        # self.sf.bind_arrow_keys(self.sf)
        # self.bind("<Control-u>", self.update_data_list)
        self.sf.bind("<Button-1>", self.on_panel_click)  # Sets focus to the panel being clicked on
        self.bind("<Button-1>", self.on_panel_click)  # Sets focus to the panel being clicked on
