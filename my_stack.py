import copy


class MyStack:
    """Stack: LIFO works with the drag_drop module
    Requires: event, initial grid_info, current target that cursor is over to push a widget onto the stack.
    start = the initial grid_info for the initially grabbed widget
    target = the current widget that the cursor is over."""

    def __init__(self):
        self.my_stack = []
        self.event = None
        self.grid_info = None
        self.row = None
        self.column = None
        self.widget = None

    def push(self, event, start, target):
        start_frame = start.get('in')       # initial widget grid_info.get('in')
        if target is not None:
            self.grid_info = target.grid_info() # current target grid_info
            # self.row = self.grid_info.get('row')
            # self.column = self.grid_info.get('column')
            target_info_in = self.grid_info.get("in")
            previous_push = self.peek()
            # print(f'prev-push: {previous_push} row: {self.row} col: {self.column}')
            if previous_push is not None:
                if start_frame == target_info_in and target != previous_push:
                    self.widget = event.widget
                    self.my_stack.append(target)
                    # print(f'my_stack-pushed: {self.my_stack} {self.show()}')
            elif previous_push is None:
                self.my_stack.append(target)


    def pop(self):
        """On release, pop the last item on the stack, then clear stack"""
        if len(self.my_stack):
            item = self.my_stack.pop()
            self.my_stack.clear()
            return item

    def peek(self):
        stack_copy = list(copy.copy(self.my_stack))
        if len(stack_copy) > 0:
            # print(f'peek: {stack_copy[-1]}')
            return stack_copy[-1]
        return

    def __len__(self):
        return len(self.my_stack)

    def show(self):
        print("Stack LIFO...")
        for item in reversed(self.my_stack):
            print(item)
