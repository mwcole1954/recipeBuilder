
class Data:

    def __init__(self, label, value):

        self.label = label
        self.value = value

    def __repr__(self):
        return f'Data: {hash(Data)} {self.label}, {self.value}'

    def __str__(self):
        return f'Data({self.label}, {self.value}'
