import unittest

from core.understander.generic import generic_question as test_file
from test.inputs.generic_question import *

class GenericQuestionTest(unittest.TestCase):

    def test_strip_question_part(self):
        for question, result in questions.items():
            q = test_file.question_analyzer(question)
            self.assertEqual(q.question_extract, result['question_extract'])
            self.assertEqual(q.category, result['category'])
            self.assertEqual(q.marker_value, result['marker_value'])

    def test_understand(self):
        for question, result in questions.items():
            question_processed_form = test_file.understand(question)
            print(question_processed_form)
            print('**********************************************************************')
            #if question_processed_form['category'] == 'what':
            #    print(question_processed_form)
            #    self.assertEqual(question_processed_form['category'], result['category'])
            #    self.assertEqual(question_processed_form['subject_phrase'], result['subject_phrase'])
            #    self.assertEqual(question_processed_form['time_phrase'], result['time_phrase'])

if __name__ == '__main__':
    unittest.main()