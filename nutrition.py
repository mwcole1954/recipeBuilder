import math
import tkinter

from scrolled_frame_alt import ScrolledFrame
from base_recipe import BaseRecipe
from drag_drop import DragDrop


class Nutrition(tkinter.LabelFrame, DragDrop, BaseRecipe):
    """Panel to hold the nutrition information for the recipe. Inherits from BaseMethods.
    Initiated from main.py and is passed the master widget, label_font and text font.
    Special_list is a conceptual idea but is not used at this point."""

    def __init__(self, master, label_font, font, em_font, special_list=None):
        super().__init__(master)
        self.save = False  # Will be True if created new data or updated a field
        self.sf = None
        self.inner_frame = None
        self.master = master
        self.data_list = []
        self.label_list = []
        self.value_list = []
        self.label_font = label_font
        self.font = font
        self.em_font = em_font
        self.config(text='Nutrients', font=self.label_font)
        self.directory = None
        self.focus = False
        self.ndx = None
        if special_list is not None:
            self.special_list = special_list
        else:
            self.special_list = ('name', 'category')

    def __repr__(self):
        return f'Nutrition: {self.data_list} {self.label_list} {self.value_list}'

    # GUI
    def make_panel(self):
        self.clear_label_value_list()

        self.config(takefocus=True, highlightcolor="blue", highlightthickness=2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=2, sticky='nsew')
        # Scroll frame to put the label and text fields into
        self.sf = ScrolledFrame(self, scrollbars="vertical")
        self.sf.columnconfigure(0, weight=1)
        self.sf.grid(row=0, column=0, sticky='nsew')
        self.inner_frame = self.sf.display_widget(tkinter.Frame, fit_width=True, padx=2)
        self.inner_frame.columnconfigure(1, weight=1)
        # Use data_list to recreate the label and value lists
        for n, data in enumerate(self.data_list):
            self.inner_frame.rowconfigure(n, weight=1)
            self.label_list.append('')
            self.label_list[n] = tkinter.Label(self.inner_frame, takefocus=True, font=self.em_font, anchor='e',
                                               width=20, height=1, padx=2)
            self.label_list[n].config(text=self.data_list[n].label.title())
            self.label_list[n].bind("<Button-1>", self.check_b1)
            self.label_list[n].bind("<ButtonRelease-1>", self.check_2b1)
            self.label_list[n].bind("<Enter>", self.on_hover)  # FOCUS IN label  Tried need to retest
            self.label_list[n].bind("<Leave>", self.on_leave)
            self.label_list[n].bind("<Return>", self.update_data_list)
            self.label_list[n].grid(row=n, column=0, sticky='ew')

            self.value_list.append('')
            ht = 1
            self.value_list[n] = tkinter.Text(self.inner_frame, width=25, height=ht, wrap=tkinter.WORD, font=self.font,
                                              takefocus=True, padx=2, undo=True, highlightcolor='black',
                                              highlightthickness=1)
            ht = math.ceil(len(self.data_list[n].value) / (self.value_list[n]['width'] + 11))
            self.value_list[n].config(height=ht)
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
        self.sf.bind("<Button-1>", self.on_panel_click)
        self.bind("<Button-1>", self.on_panel_click)