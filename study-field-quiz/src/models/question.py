class Question:
    def __init__(self, question_text, answer_options):
        self.question_text = question_text
        self.answer_options = answer_options

    def get_question(self):
        return self.question_text

    def get_answer_options(self):
        return self.answer_options