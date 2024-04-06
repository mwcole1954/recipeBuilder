from abc import ABC
from tkinter import Label, Text
from my_stack import MyStack
from base_recipe import BaseRecipe

stack = MyStack()


class DragDrop(BaseRecipe, ABC):
    def __init__(self):
        super().__init__()

    def finish_up(self, target, widget, initial):

        # Original position of the grabbed widget to find in data lists
        w_row = initial.get('row')
        t_row = target.grid_info().get('row')  # t_row: target row for widget
        # t_row = target.grid_info().get('row')
        if t_row is not None and 0 <= t_row < len(self.label_list) and 0 <= w_row < len(self.label_list):
            if isinstance(widget, Text) or isinstance(widget, Label):
                if t_row < w_row:
                    w = self.value_list.pop(w_row)
                    l_w = self.label_list.pop(w_row)
                    self.label_list.insert(t_row, l_w)
                    self.value_list.insert(t_row, w)
                elif w_row < t_row < len(self.label_list) - 1:
                    l_w = self.label_list[w_row]
                    w = self.value_list[w_row]
                    self.label_list.insert(t_row + 1, l_w)
                    self.value_list.insert(t_row + 1, w)
                    self.label_list.pop(w_row)
                    self.value_list.pop(w_row)
                elif t_row > w_row and t_row == len(self.label_list) - 1:
                    l_w = self.label_list[w_row]
                    w = self.value_list[w_row]
                    self.label_list.append(l_w)
                    self.value_list.append(w)
                    self.label_list.pop(w_row)
                    self.value_list.pop(w_row)

            self.update_data_list()
            self.make_panel()

    def on_click(self, event):
        """Get the widget clicked, determine initial grid_info, set focus to clicked widget"""
        widget = event.widget
        widget.focus_set()
        widget.config(fg='gray')
        grid_info = event.widget.grid_info()

        # print(event)
        if event.num == 3:
            if isinstance(widget, Text) or isinstance(widget, Label):
                widget.config(cursor='double_arrow')
        elif event.num == 1:
            if isinstance(widget, Label):
                widget.config(cursor='exchange')
        else:
            widget.config(cursor='arrow')

        """Get the widget grabbed, get initial grid_info, set focus to grabbed widget"""
        if isinstance(widget, Label) or isinstance(widget, Text):
            widget.bind("<B1-Motion>", lambda event: self.drag(event, widget, grid_info))
            widget.bind("<ButtonRelease-1>", lambda event: self.release(event, widget, grid_info))
        else:
            event.widget.unbind("<ButtonRelease-1")

    def drag(self, event, widget, initial_info):
        if isinstance(event.widget, Label) or isinstance(event.widget, Text):
            event.widget.config(cursor="double_arrow")
            widget.lift()

            w_row = widget.grid_info().get('row')  # w_row: starting widget row
            target = widget.winfo_containing(*widget.winfo_pointerxy())  # target widget
            # print(f'target: {target.grid_info()} self: {self} event: {event}')
            if target and target.winfo_parent() == widget.winfo_parent() and target.__class__ is widget.__class__:
                t_row = target.grid_info().get('row')  # t_row: target row for widget
                if isinstance(widget, Text):
                    # label for widget at initial row
                    l_w = self.label_list[initial_info.get('row')]  # l_w: label for widget
                    l_t = ''  # l_t: label for target
                    # get the label by finding value in list
                    for n, item in enumerate(self.value_list):
                        if target == item:
                            l_t = self.label_list[n]
                    """Showing the list while dragging the widget towards new target
                    This does not make any permanent changes to the data, which is done in finish_up()"""
                    if t_row is not None and t_row >= 0:
                        l_w.grid(row=t_row, column=0)
                        widget.grid(row=t_row, column=1)
                        l_t.grid(row=w_row, column=0)
                        target.grid(row=w_row, column=1)

                elif isinstance(widget, Label):
                    # v_w: value for widget from initial grid_info (correlates with current lab_val_list
                    v_w = self.value_list[initial_info.get('row')]
                    v_t = ''
                    # get the value by finding label in list
                    for n, item in enumerate(self.label_list):
                        if target == item:
                            v_t = self.value_list[n]
                    widget.grid(row=t_row, column=0)
                    v_w.grid(row=t_row, column=1)
                    target.grid(row=w_row, column=0)
                    v_t.grid(row=w_row, column=1)
                # push the current target widget
                stack.push(event, initial_info, target)

    def release(self, event, widget, initial):
        widget.config(fg='black')
        # target = widget.winfo_containing(*widget.winfo_pointerxy())
        # pop the last widget on the stack and finish up
        target = stack.pop()
        self.finish_up(target, widget, initial)
