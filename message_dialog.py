import tkinter


class MyMessageDialog(tkinter.Frame):
    """
    The class for showing the user a message.
    *args accepts the prompt cues based on what information the panel needs.
    Returns --> None
    **kwargs: font, label_font, title_font
    """

    def __init__(self, master, title, message=None, *args, **kwargs):
        super().__init__(master)

        self.result = ()
        self.box = []
        self.box_text = []
        self.master = master
        self.title = title
        self.message = message
        self.font = kwargs.get('font', ('Mono', 12, 'normal'))
        self.title_font = kwargs.get('title_font', ('Mono', 14, 'bold'))
        self.label_font = kwargs.get('label_font', ('Mono', 12, 'bold'))
        self.text_height = kwargs.get('text_height', 2)

        self.config(pady=5, padx=10)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.grid(row=0, column=0, sticky='nsew')
        # Make the title label
        if len(title.strip()) > 0:
            label = tkinter.Label(self, text=self.title, relief='groove',
                                  highlightthickness=0, font=self.title_font)
            label.grid(row=0, column=0, columnspan=2, sticky='ew', pady=2, padx=5)
        # The message
        text_box = tkinter.Text(self, width=50, height=self.text_height, pady=2, padx=2,
                                font=self.font, wrap=tkinter.WORD, spacing1=10)
        text_box.tag_add('center', 1.0, tkinter.END)
        text_box.tag_config('center', justify='center')
        text_box.insert(1.0, self.message, 'center')
        text_box.grid(row=1, column=0, sticky='nsew')

        submit_but = tkinter.Button(self, text='Close', command=self.close)
        submit_but.grid(row=6, column=0, columnspan=2, sticky='s')

        self.master.bind("<Return>", self.close)
        submit_but.focus_set()

        self.mainloop()

    def do_these(self):
        # Submit button pressed
        self.get_values()
        return self.result

    def get_values(self):
        self.result = self.box_text

    def close(self, event=None):
        self.grab_release()
        self.master.quit()


def show_message(title=None, message=None, *args, **kwargs):
    # t_root = tkinter.Tk()
    t_root = tkinter.Toplevel()
    t_root.geometry("+500+250")
    MyMessageDialog(t_root, title, message, *args, **kwargs)
    print("destroy")
    t_root.destroy()





if __name__ == "__main__":
    show_message("My Message", "Don't forget to shut off the water.")
