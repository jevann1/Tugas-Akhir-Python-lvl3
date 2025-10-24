from tkinter import Tk, Label, Button, StringVar, OptionMenu, messagebox
import json

class QuizWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Study Field Quiz")

        self.question_label = Label(master, text="What field of study do you prefer?")
        self.question_label.pack(pady=20)

        self.selected_field = StringVar(master)
        self.selected_field.set("Select your field")

        self.fields = ["Science", "Arts", "Commerce", "Engineering", "Medicine"]
        self.field_menu = OptionMenu(master, self.selected_field, *self.fields)
        self.field_menu.pack(pady=10)

        self.submit_button = Button(master, text="Submit", command=self.submit_answer)
        self.submit_button.pack(pady=20)

    def submit_answer(self):
        selected = self.selected_field.get()
        if selected == "Select your field":
            messagebox.showwarning("Warning", "Please select a field of study.")
        else:
            messagebox.showinfo("Selected Field", f"You selected: {selected}")
            # Here you can add functionality to handle the selected answer

def load_questions():
    with open('src/data/questions.json') as f:
        return json.load(f)

if __name__ == "__main__":
    root = Tk()
    quiz_window = QuizWindow(root)
    root.mainloop()