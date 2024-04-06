import tkinter


class MyMessageDialog(tkinter.Frame):
    """
    The class for getting a yes or no type of response from the user.
    Returns the boolean: YES==True or NO==False
    **kwargs: font=('Arial', 12, 'normal') is the default; title_font=('Arial', 12, 'bold')
    and button_font=('Arial', 8 'bold')  as the defaults.
    """

    def __init__(self, master, title='', message='', *args, **kwargs):
        super().__init__(master)

        self.result = None
        self.box = []
        self.box_text = []
        self.master = master
        self.title = title
        self.message = message
        self.font = kwargs.get('font', ('Arial', 12, 'normal'))
        self.title_font = kwargs.get('title_font', ('Arial', 14, 'bold'))
        self.button_font = kwargs.get('button_font', ('Arial', 8, 'bold'))

        self.config(pady=5, padx=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky='nsew')
        # Make the title label
        if len(title.strip()) > 0:
            label = tkinter.Label(self, text=self.title, relief='groove', borderwidth=2,
                                  highlightthickness=0, font=self.title_font)
            label.grid(row=0, column=0, columnspan=2, sticky='ew', pady=2, padx=5)
        # The message
        ht = 3 if len(self.message) < 50 else 5
        text_box = tkinter.Text(self, width=50, height=ht, pady=2, padx=2,
                                font=self.font, bg='gray93', fg="black", wrap=tkinter.WORD)
        text_box.tag_add('center', 1.0, tkinter.END)
        text_box.tag_config('center', justify='center')
        text_box.insert(1.0, self.message, 'center')
        text_box.grid(row=1, column=0, sticky='nsew')

        but_frame = tkinter.Frame(self)
        but_frame.columnconfigure(0, weight=1)
        but_frame.columnconfigure(1, weight=1)
        submit_but = tkinter.Button(but_frame, text='YES', width=3, font=self.button_font, command=self.do_these)
        submit_but.grid(row=2, column=0, sticky='se', padx=20, ipadx=5)
        cancel_but = tkinter.Button(but_frame, text="NO", width=3, font=self.button_font, command=self.cancel)
        cancel_but.grid(row=2, column=1, sticky='sw', padx=20, ipadx=5)
        but_frame.grid(row=2, column=0, sticky='nsew')

        master.grab_set()

        master.mainloop()

    def do_these(self):
        # Submit button pressed
        self.get_values(True)
        self.close()

    def cancel(self):
        self.get_values(False)
        self.close()

    def get_values(self, answer):
        self.result = answer
        return self.result

    def close(self):
        self.quit()


def show_yes_no(title='', message='', *args, **kwargs):
    t_root = tkinter.Toplevel()
    t_root.geometry("+500+250")
    d = MyMessageDialog(t_root, title, message, *args, **kwargs)
    t_root.destroy()
    return d.result


if __name__ == "__main__":
    # t_root = tkinter.Tk()
    response = show_yes_no("The Information", "Do you want to do this...")
    print(f'response: {response}')
