

class Player:

    def __init__(self, name, color):
        self.name = name
        self.counter = 0
        self.color = color

    def increase_counter(self, quantity=1):
        self.counter += quantity

    def restart_counter(self):
        self.counter = 0
