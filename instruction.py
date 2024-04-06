import math
import tkinter

from scrolled_frame_alt import ScrolledFrame
from base_recipe import BaseRecipe
from drag_drop import DragDrop


class Instruction(tkinter.LabelFrame, DragDrop, BaseRecipe):
    """Panel to hold the instruction information for the recipe. Inherits from BaseMethods.
        Initiated from main.py and is passed the master widget, label_font and text font.
        Special_list is a conceptual idea but is not used at this point."""

    def __init__(self, master, label_font, font, em_font):
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
        self.config(text='Instructions', font=self.label_font)
        self.directory = None
        self.focus = False
        self.ndx = None

    def __repr__(self):
        return f'Instruction: {self.data_list} {self.label_list} {self.value_list}'

    # GUI
    def make_panel(self):
        self.clear_label_value_list()

        self.config(takefocus=True, highlightcolor="blue", highlightthickness=2)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky='nsew')
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
            self.label_list[n] = tkinter.Label(self.inner_frame, font=self.em_font, takefocus=False, anchor='e')
            self.label_list[n].config(text=self.data_list[n].label.title())
            self.label_list[n].grid(row=n, column=0, sticky='e')
            self.label_list[n].bind("<Button-1>", self.on_panel_click)
            self.value_list.append('')
            ht = 1
            self.value_list[n] = tkinter.Text(self.inner_frame, width=100, height=ht, wrap=tkinter.WORD,
                                              font=self.font, undo=True, highlightcolor='black', highlightthickness=1,
                                              takefocus=True, padx=2)
            ht = math.ceil(len(self.data_list[n].value) / (self.value_list[n]['width'] + 30))
            self.value_list[n].config(height=ht)
            # Split the text by '. ' and then join
            t_list = data.value.split('. ')
            txt = '. '.join(f'{item[0].capitalize()}{item[1:]}' for item in t_list)
            txt = txt.replace(' f ', ' F ')
            txt = txt.replace(' f.', ' F.')
            txt = txt.replace('degrees c', 'degrees C')
            self.value_list[n].insert(1.0, txt)

            self.value_list[n].bind("<Enter>", self.on_hover)
            self.value_list[n].bind("<Leave>", self.on_leave)
            self.value_list[n].bind("<Return>", self.update_data_list)
            self.value_list[n].bind("<Button-1>", self.check_b1)
            self.value_list[n].bind("<Double-Button-1>", self.check_2b1)
            self.value_list[n].grid(row=n, column=1, sticky='ew')

        self.sf.bind("<Enter>", lambda _: self.sf.bind_scroll_wheel(self.sf.c))
        self.sf.bind("<Leave>", self.sf.c.unbind_all("<MouseWheel>"))
        self.sf.bind("<Button-1>", self.on_panel_click)
        self.bind("<Button-1>", self.on_panel_click)

# if __name__ == "__main__":
#     import os
#
#     root = tkinter.Tk()
#     root.columnconfigure(0, weight=1)
#     root.rowconfigure(0, weight=1)
#     ins = Instruction(root, ("Arial", 14, "bold"), ("Arial", 12, "normal"))
#     ins.make_panel()
#     ins.read_file(os.path.join(os.getcwd(), "Recipes", "Gingerbread Cookies"))
#     ins.make_panel()
#
#     root.mainloop()
