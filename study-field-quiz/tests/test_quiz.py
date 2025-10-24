import unittest
from src.models.question import Question

class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.question = Question("What is your favorite field of study?", ["Science", "Arts", "Commerce", "Engineering"])

    def test_question_text(self):
        self.assertEqual(self.question.text, "What is your favorite field of study?")

    def test_question_answers(self):
        self.assertEqual(self.question.answers, ["Science", "Arts", "Commerce", "Engineering"])

    def test_question_answer_count(self):
        self.assertEqual(len(self.question.answers), 4)

if __name__ == '__main__':
    unittest.main()