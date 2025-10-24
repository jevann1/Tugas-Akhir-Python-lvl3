from tkinter import Button, Label, Frame

class QuizButton(Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(padx=10, pady=5, bg='lightblue', fg='black', font=('Arial', 12))

class QuizLabel(Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg='white', fg='black', font=('Arial', 14))

class QuizFrame(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg='white')