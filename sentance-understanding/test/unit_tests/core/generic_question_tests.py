import unittest

from core.generic import generic_question as test_file
from test.inputs.generic_question import *

class GenericQuestionTest(unittest.TestCase):

    def test_strip_question_part(self):
        for question, result in questions.items():
            q = test_file.question_analyzer(question)
            self.assertEquals(q.question_extract, result['question_extract'])
            self.assertEquals(q.category, result['category'])
            self.assertEquals(q.marker_value, result['marker_value'])

    def test_understand(self):
        for question, result in questions.items():
            question_processed_form = test_file.understand(question)
            print(question_processed_form)
            self.assertEquals('1', '1')

if __name__ == '__main__':
    unittest.main()