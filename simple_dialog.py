# This is a good class so far
# Do not lose this one
import tkinter
from tkinter.ttk import Frame, Label, Entry, Button


# Good habit to put your GUI in a class to make it self-contained
class MySimpleDialog(Frame):
    """
    Allows asking one or more prompts to get one or more user inputs.
    Also allows submitting a default_val to enter the next position number when adding fields
    to the ingredients and instructions panels.

    Returns a list containing user responses or 'Cancel'
    :rtype: returns list of response(s) or "Cancel"
    Will need to test for the length of the returned list
    *args accept the user prompts
    **kwargs accept font, label_font, title_font, default_val
    Default_val= is the current item number in ingredients or instructions when adding
    a new field value. The label is automatically entered but can be changed.
    """

    def __init__(self, master, title, *args, **kwargs):
        super().__init__(master)

        # self allow the variable to be used anywhere in the class
        self.dialog_menu = None
        self.result = []
        self.prompts = []
        self.entry = []
        self.master = master
        self.title = title
        for prompt in args:
            self.prompts.append(prompt)
        # kwarg values if available or default
        self.initial_value = kwargs.get('initial_value', '')
        self.temp_val = kwargs.get('default_val', '')
        self.font = kwargs.get('font', ("Arial", 12, 'normal'))
        self.label_font = kwargs.get('label_font', ("Arial", 12, 'bold'))
        self.title_font = kwargs.get('title_font', ("Arial", 14, 'bold'))

        self.init_ui()

    def init_ui(self):
        # Title frame
        self.config(padding=(10, 0))
        t_frame = tkinter.Frame(self, relief='flat')
        t_frame.grid(row=0, column=0, sticky='ew')
        Label(t_frame, text=self.title, font=self.title_font, anchor='n', justify="center",
              padding=(0, 0, 0, 10)).grid(row=0, column=0, sticky='ew')
        tkinter.ttk.Separator(t_frame, orient=tkinter.HORIZONTAL).grid(row=1, column=0, sticky='ew')

        # Prompts and entry boxes for 1 to many
        frame1 = tkinter.Frame(self, borderwidth=2, highlightcolor='grey80', highlightthickness=2,
                               relief='groove', padx=5)
        frame1.grid(row=1, column=0, sticky='nsew')
        x = 0
        for n, item in enumerate(self.prompts):
            Label(frame1, text=item, justify='center',
                  font=self.label_font).grid(row=x, column=0, sticky='s', padx=10)
            self.entry.append('')
            self.entry[n] = Entry(frame1, width=50, font=self.font, justify=tkinter.CENTER)
            if self.temp_val and n == 0 and len(self.prompts) > 1:
                self.entry[n].insert(0, self.temp_val)
            elif self.temp_val and n == 0 and len(self.prompts) == 1:
                self.entry[n].insert(0, self.temp_val)
            self.entry[n].grid(row=x + 1, column=0, sticky='sew')
            self.entry[n].bind("<Return>", self.next_focus)
            self.entry[n].bind("<Button-3>", func=self.show_dialog)
            x += 2

        # frame2 contains the submit button
        frame2 = tkinter.Frame(self, borderwidth=0, highlightcolor='grey80', highlightthickness=0,
                               relief='flat', padx=5)
        frame2.grid(row=2, column=0, sticky='sew', pady=10)
        # Command tells the form what to do when the button is clicked
        btn = Button(frame2, text="Submit", command=self.on_submit)
        btn.grid(row=0, column=0, sticky='s')
        quit_btn = Button(frame2, text="Cancel", command=self.on_cancel)
        quit_btn.grid(row=0, column=1, sticky='s')

        # Make Menu
        self.dialog_menu = tkinter.Menu(self.master, tearoff=False)
        self.dialog_menu.add_command(label="Copy", command=self.copy)
        self.dialog_menu.add_command(label="Paste", command=self.paste)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        t_frame.columnconfigure(0, weight=1)
        frame2.columnconfigure(0, weight=1)
        frame2.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky='nsew')

        # give the first entry field focus if no temp_val
        if self.temp_val and len(self.prompts) > 1:
            # set focus in second entry widget
            self.entry[1].focus_set()
        else:
            # set focus in the first entry widget
            self.entry[0].focus_set()
            self.entry[0].select_range(start=0, end=tkinter.END)

        self.master.grab_set()
        # Bind the root to the Enter key to call on_submit
        self.master.bind("<Return>", func=self.on_submit)

    def show_dialog(self, event=None):
        self.dialog_menu.tk_popup(event.x_root, event.y_root)

    def copy(self, event=None):
        txt = self.entry[1].get()
        self.master.clipboard_clear()
        self.master.clipboard_append(txt)

    def paste(self, event=None):
        txt = self.master.clipboard_get()
        self.entry[1].insert(1, txt)

    def on_tab(self, event):
        if isinstance(event.widget, Entry):
            event.widget.delete(0, tkinter.END)

    def next_focus(self, event):
        for item in self.entry:
            if isinstance(event, tkinter.Event):
                if item == event.widget:
                    item.tk_focusNext().focus()
                    return "break"
            elif isinstance(event, tkinter.Entry):
                if item == event:
                    item.tk_focusNext().focus()
                    return "break"

    def on_cancel(self, *args):
        self.result.clear()
        self.result.append('Cancel')
        self.master.quit()

    def on_submit(self, *args):
        self.result.clear()
        for item in self.entry:
            self.result.append(item.get())
        self.master.quit()


# Centers the dialog window to the middle of the computer screen
def get_screen_center():
    # Don't need Tk(), only need Toplevel()
    # Create Toplevel and center it
    master = tkinter.Toplevel()
    master.config(takefocus=True)
    width = 300
    height = 200
    master.geometry("+{}+{}".format(master.winfo_screenwidth() // 2 - width // 2,
                                    master.winfo_screenheight() // 2 - height //
                                    2))
    return master


# This asks for more than one prompt
def ask_strings(title, *args, **kwargs):
    """
    :ptype: html from recipe website
    :rtype: list
    """
    # This part triggers the dialog
    master = get_screen_center()
    # master.title(title)
    app = MySimpleDialog(master, title, *args, **kwargs)
    master.mainloop()
    # Here we can act on the form components or
    # better yet, copy the output to a new variable
    # sets user_input to the same reference id as result
    user_input = app.result
    # print(app.output1)
    # Get rid of the error message if the user clicks the
    # close icon instead of the submit button
    # Any component of the dialog will no longer be available
    # past this point
    try:
        master.destroy()
    except:
        pass
    # To use data outside of function
    # Can either be used in __main__
    # or by external script depending on
    # what calls main()
    return user_input


if __name__ == "__main__":
    result = ask_strings("My Title", "Prompt1", "Prompt2", default_val=1)
    print(f'result: {result}')
