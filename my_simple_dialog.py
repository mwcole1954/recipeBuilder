# This is a good class so far
# Do not lose this one
import tkinter
from tkinter.ttk import Frame, Label, Entry, Button

# CONSTANTS
FONT = ("Arial", 12, 'normal')
LABEL_FONT = ("Arial", 12, 'bold')
LABEL_FRAME_FONT = ("Arial", 18, 'bold')


# Good habit to put your GUI in a class to make it self-contained
class MySimpleDialog(Frame):
    """
    Allows asking one or more prompts to get one or more user inputs.
    Will need to test for the length of the returned list
    """

    def __init__(self, master, title, *args, default_val):
        super().__init__(master)

        # self allow the variable to be used anywhere in the class
        self.result = []
        self.prompts = []
        self.entry = []
        self.temp_val = default_val
        self.master = master
        self.title = title

        for prompt in args:
            self.prompts.append(prompt)

        self.init_ui()

    def init_ui(self):

        # Title frame
        self.config(padding=(10, 0))
        t_frame = Frame(self)
        t_frame.grid(row=0, column=0, sticky='nsew')
        Label(t_frame, text=self.title, font=LABEL_FRAME_FONT, anchor='n', justify="center",
              padding=(0, 0, 0, 10)).grid(row=0, column=0, sticky='ew')
        tkinter.ttk.Separator(t_frame, orient=tkinter.HORIZONTAL).grid(row=1, column=0, sticky='ew')

        # Prompts and entry boxes for 1 to many
        frame1 = Frame(self)
        frame1.grid(row=1, column=0, sticky='nsew')
        x = 0
        for n, item in enumerate(self.prompts):
            Label(frame1, text=item, padding=5, font=LABEL_FONT).grid(row=x, column=0, sticky='sew')
            self.entry.append('')
            self.entry[n] = Entry(frame1, width=35, font=FONT)
            if n == 0 and self.temp_val:
                self.entry[n].insert(0, self.temp_val)
            self.entry[n].grid(row=x + 1, column=0, sticky='sew')
            self.entry[n].bind("<Return>", self.next_focus)
            x += 2

        # frame2 contains the submit button
        frame2 = Frame(self)
        frame2.grid(row=2, column=0, sticky='sew', pady=10)
        # Command tells the form what to do when the button is clicked
        btn = Button(frame2, text="Submit", command=self.on_submit)
        btn.grid(row=0, column=0, sticky='s')
        quit_btn = Button(frame2, text="Cancel", command=self.on_cancel)
        quit_btn.grid(row=0, column=1, sticky='s')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        t_frame.columnconfigure(0, weight=1)
        frame2.columnconfigure(0, weight=1)
        frame2.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky='nsew')

        # give the first entry field focus
        self.entry[0].focus_set()
        self.master.grab_set()

        # Bind the root to the Enter key to call on_submit
        self.master.bind("<Return>", func=self.on_submit)

    def next_focus(self, event):
        for item in self.entry:
            if item == event.widget:
                item.tk_focusNext().focus()
                return "break"

    def on_cancel(self, *args):
        self.result.clear()
        self.result.append('Cancel')
        self.quit()

    def on_submit(self, *args):
        self.result.clear()
        for item in self.entry:
            self.result.append(item.get())
        self.quit()


# Centers the dialog window to the middle of the computer screen
def get_screen_center():
    # Don't need Tk(), only need Toplevel()
    # root = tkinter.Tk()
    # root.withdraw()
    master = tkinter.Toplevel()
    master.config(takefocus=True)
    width = 300
    height = 200
    master.geometry("+{}+{}".format(master.winfo_screenwidth() // 2 - width // 2,
                                    master.winfo_screenheight() // 2 - height //
                                    2))
    return master


# This asks for more than one prompt
def ask_strings(title, *args, default_val=''):
    # This part triggers the dialog
    master = get_screen_center()
    # master.title(title)
    app = MySimpleDialog(master, title, *args, default_val=default_val)
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
    result = ask_strings("My Title", "Prompt1", "Prompt2", "Prompt3")
    print(result)
