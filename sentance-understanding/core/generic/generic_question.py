import nltk
from core.generic.question_category_dict import *

class Analyzer:
    def get_handler(self, handler_type):
        handler_name = '_'.join(handler_type.lower().split(' '))
        return getattr(self, handler_name + '_handler', None)

    def what_handler(self, ):
        pass

    def when_handler(self):
        pass

    def where_handler(self):
        pass

    def why_handler(self):
        pass

    def who_handler(self):
        pass

    def boolean_handler(self):
        pass

    def count_hanlder(self):
        pass

def understand(text):
    question = question_analyzer(text)
    import os
    grammar_file = os.path.join(os.path.dirname(__file__), '../../grammars/generic_question', question.category)
    with open(grammar_file, 'r') as file:
        grammar_str = file.read()
    question_processed_form = {
        'category': None,
        'subject_phrase': None,
        'time_phrase': None,
        'actual_question': text
    }
    if question.category == 'what':
        grammar = nltk.PCFG.fromstring(grammar_str)
        parser = nltk.ViterbiParser(grammar)
        #parser.trace()
        question_processed_form['category'] = question.category
        trees = parser.parse(question.question_extract)
        for tree in trees:
            subject_phrase = tree_iterator(tree, 'SUBJECT_PHRASE').leaves()
            subject_phrase = ''.join(subject_phrase)
            time = tree_iterator(tree, 'TIME_PHRASE').leaves()
            time = ''.join(time)
            question_processed_form['subject_phrase'] = subject_phrase
            question_processed_form['time_phrase'] = time

    return question_processed_form

def tree_iterator(tree, label):
    value = None
    for a in tree:
        if isinstance(a, str):
            continue
        if a.label() == label:
            value = a
            break
        else:
            temp = tree_iterator(a, label)
            if temp is not None:
                value = temp
    return value


def question_analyzer(text):
    import re
    selected_marker = selected_category = question_extract = None
    # question_markers = question_category.keys()
    for marker in question_markers:
        if re.search(marker, text):
            selected_marker = marker
            selected_category = question_category[selected_marker]
            question_extract = text[text.index(selected_marker):]
            break

    from collections import namedtuple
    Question = namedtuple('Question', ['category', 'marker_value', 'question_extract','actual_question'])
    question = Question(category=selected_category,
                        marker_value=selected_marker,
                        question_extract=question_extract,
                        actual_question=text)
    return question
