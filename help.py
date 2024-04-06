import tkinter


class Help(tkinter.Frame):
    FONT = ("Arial", 12, 'normal')

    def __init__(self, master):
        super().__init__(master)

        self.help_file = ''
        self.read_help_file()

    def make_panel(self):
        title = tkinter.Label(self, text="Recipe Builder Help")
        title.grid(row=0, column=0, sticky='ew')

        vbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        vbar.grid(row=1, column=1, sticky='ns')

        notepad = tkinter.Text(self, padx=5, pady=5, width=80, wrap='word', font=Help.FONT, state="disabled",
                               yscrollcommand=vbar.set)
        notepad.insert(1.0, self.help_file)
        notepad.grid(row=1, column=0, sticky='nsew')

        vbar.config(command=notepad.yview)
        bottom = tkinter.Frame(self)
        bottom.grid(row=2, column=0, sticky='ew')
        self.grid(row=0, column=0, sticky='nsew')
        quit_but = tkinter.Button(bottom, text="CLOSE", command=self.close_notepad)
        quit_but.grid(row=0, column=0, columnspan=2, sticky='ew')
        quit_but.bind("<Enter>", self.enter)
        quit_but.bind("<Leave>", self.leave)

    def close_notepad(self):
        self.destroy()
        exit()

    # Button Enter Leave with cursor/
    @staticmethod
    def enter(event):
        event.widget['bg'] = 'gray'
        event.widget['fg'] = 'azure'

    @staticmethod
    def leave(event):
        event.widget['bg'] = 'gray90'
        event.widget['fg'] = 'black'

    def read_help_file(self):
        with open('help.txt', 'r') as fp:
            self.help_file = fp.read()

if __name__ == "__main__":
    top = tkinter.Toplevel()
    top.title("Recipe Builder Help")
    top.geometry("1100x700+300+50")
    app = Help(top)
    app.make_panel()
    top.mainloop()
