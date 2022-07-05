from overlay import overlay

class Parent:
    def name(self):
        return 'Parent'

    def ident(self):
        who = self.name()
        print(f'Parent says: my name is {who}')

class Child(Parent):
    def say_supername(self):
        super().ident()

    def say_name(self):
        self.ident()

    def ident(self):
        who = self.name()
        print(f'Child says: my name is {who}')

    def name(self):
        return 'Bob'

class Overlay:
    def name(self):
        return 'Overlay'

Child().say_name()
Child().say_supername()
overlay(Overlay, Child()).say_name()
overlay(Overlay, Child()).say_supername()
