# This is a good class so far
# Do not lose this one
import tkinter
from tkinter.ttk import Frame, Label, Entry, Button


# Good habit to put your GUI in a class to make it self-contained
class SearchDialog(Frame):
    """
    Presents the user with a choice of two radiobuttons and an entry box.
    The user checks the appropriate search button and then enters the search criteria.
    These can be seperated by spaces or commas.
    The search choice, 'category' is the default and the cursor starts in the entry box
    :command: call function ask_strings(<title>, <prompt>)
    :parameter: <title> is the title for the dialog; <prompt> is the information being requested.
    :rtype: list | 'Cancel'
        """

    def __init__(self, master, title, prompt):
        super().__init__(master)

        # self allow the variable to be used anywhere in the class
        self.rb2 = None
        self.rb1 = None
        self.submit_btn = None
        self.result = []
        self.master = master
        self.title = title
        self.prompt = prompt
        self.entry = None
        self.rb = None
        self.entry_var = tkinter.StringVar()

        self.init_ui()

    def init_ui(self):
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        # Title frame
        self.config(padding=(10, 0))
        t_frame = tkinter.Frame(self, relief='flat')
        t_frame.grid(row=0, column=0, sticky='ew')
        style = tkinter.ttk.Style(t_frame)
        style.configure('TLabel', font=("Arial", 14, 'bold'))
        tkinter.ttk.Label(t_frame, text=self.title, anchor='n', justify="center",
                          padding=(0, 0, 0, 10), relief='groove').grid(row=0, column=0, sticky='ew')
        tkinter.ttk.Separator(t_frame, orient=tkinter.HORIZONTAL).grid(row=1, column=0, sticky='ew', pady=4)

        # Checkboxes for Category and Ingredients search selection

        frame1 = tkinter.Frame(self, borderwidth=2, highlightcolor='grey80', highlightthickness=2,
                               relief='groove', padx=5)
        frame1.grid(row=1, column=0, sticky='nsew')
        # styles for frame1 widgets
        style = tkinter.ttk.Style(frame1)
        style.configure("TRadiobutton", font=("Arial", 10, 'normal'))
        style.configure("TLabel", font=("Arial", 12, 'bold'))

        tkinter.ttk.Label(frame1, text="Search by Category or Ingredients: ").grid(row=0, column=0, sticky='ew')
        self.rb = tkinter.StringVar(frame1, 'Category')
        self.rb1 = tkinter.ttk.Radiobutton(frame1, text='Category', variable=self.rb, value='Category',
                                command=self.check)
        self.rb1.grid(row=1, column=0, sticky='w')
        self.rb2 = tkinter.ttk.Radiobutton(frame1, text='Ingredient', variable=self.rb, value='Ingredient',
                                command=self.check)
        self.rb2.grid(row=1, column=1, sticky='we')
        # self.rb1.bind("<Return>", self.next_focus)
        # self.rb2.bind("<Return>", self.next_focus)

        tkinter.ttk.Separator(frame1, orient=tkinter.HORIZONTAL).grid(row=2, column=0,
                                                                      columnspan=2, sticky='ew', pady=4)
        tkinter.ttk.Label(frame1, text=f'{self.prompt}').grid(row=3, column=0, sticky='w')
        self.entry = tkinter.ttk.Entry(frame1, width=35, justify=tkinter.CENTER,
                                       textvariable=self.entry_var, font=("Arial", 12, 'normal'))
        self.entry.grid(row=4, column=0, columnspan=2, sticky='ew', pady=4)
        self.entry.bind("<Return>", self.next_focus)

        # frame2 contains the submit and cancel buttons
        frame2 = tkinter.Frame(self, borderwidth=0, highlightcolor='grey80', highlightthickness=0,
                               relief='flat', padx=5)
        frame2.grid(row=2, column=0, sticky='sew', pady=10)
        # Command tells the form what to do when the button is clicked
        style = tkinter.ttk.Style(frame2)
        style.configure("TButton", font=("Arial", 10, 'normal'))
        self.submit_btn = Button(frame2, text="Submit", command=self.on_submit)
        self.submit_btn.grid(row=0, column=0, sticky='s')
        quit_btn = Button(frame2, text="Cancel", command=self.on_cancel)
        quit_btn.grid(row=0, column=1, sticky='s')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        t_frame.columnconfigure(0, weight=1)
        frame1.rowconfigure(0, weight=1)
        frame1.rowconfigure(1, weight=1)
        frame1.columnconfigure(0, weight=1)
        frame1.columnconfigure(1, weight=1)
        frame1.rowconfigure(2, weight=1)
        frame1.rowconfigure(3, weight=1)
        frame1.rowconfigure(4, weight=1)
        frame2.columnconfigure(0, weight=1)
        frame2.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky='nsew')

        # Bind the root to the Enter key to call on_submit
        self.submit_btn.bind("<Return>", func=self.on_submit)
        self.entry.focus_set()
        self.master.grab_set()

    def on_cancel(self, *args):
        self.result.clear()
        self.result.append('Cancel')
        self.quit()

    def check(self):
        pass

    def next_focus(self, event):
        if isinstance(self.rb1, tkinter.Radiobutton) or isinstance(self.rb2, tkinter.Radiobutton):
            self.entry.focus_set()
        elif isinstance(self.entry, tkinter.Entry):
            self.entry.tk_focusNext().focus()
            return "break"

    def on_submit(self, *args):
        self.result.clear()
        self.result.append(self.rb.get())
        self.result.append(self.entry.get())
        self.quit()


# Centers the dialog window to the middle of the computer screen
def get_screen_center():
    # Don't need Tk(), only need Toplevel()
    master = tkinter.Toplevel()
    master.config(takefocus=True)
    master.rowconfigure(0, weight=1)
    master.columnconfigure(0, weight=1)
    width = 300
    height = 200
    master.geometry("+{}+{}".format(master.winfo_screenwidth() // 2 - width // 2,
                                    master.winfo_screenheight() // 2 - height //
                                    2))
    return master


# This asks for more than one prompt
def ask_strings(title, prompt):
    # This part triggers the dialog
    master = get_screen_center()
    # master.title(title)
    app = SearchDialog(master, title, prompt=prompt)
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
    result = ask_strings("My Title", "Enter your desired criteria...")
    print(result)
