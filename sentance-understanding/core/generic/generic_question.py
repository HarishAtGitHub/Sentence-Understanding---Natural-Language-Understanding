import nltk
from core.generic.question_category_dict import *

class Analyzer:
    def __init__(self, question):
        self.question = question
        self.question_processed_form = {
            'category': question.category,
            'actual_question' : question.actual_question
        }

    def get_handler(self, handler_type):
        handler_name = '_'.join(handler_type.lower().split(' '))
        return getattr(self, handler_name + '_handler', None)

    def what_handler(self):
        #print('what')
        # TODO: FIXME: fix what grammar if and if not divider is there
        trees = self.get_processed_trees()
        for tree in trees:
            subject_phrase = tree_iterator(tree, 'SUBJECT_PHRASE').leaves()
            subject_phrase = ''.join(subject_phrase)
            time = tree_iterator(tree, 'TIME_PHRASE').leaves()
            time = ''.join(time)
            self.question_processed_form['subject_phrase'] = subject_phrase
            self.question_processed_form['time_phrase'] = time
        return self.question_processed_form

    def when_handler(self):
        #print('when')
        trees = self.get_processed_trees()
        for tree in trees:
            subject_phrase = tree_iterator(tree, 'SUBJECT_PHRASE').leaves()
            subject_phrase = ''.join(subject_phrase)
            self.question_processed_form['subject_phrase'] = subject_phrase
            time_phrase = tree_iterator(tree, 'TIME_PHRASE').leaves()
            time_phrase = ''.join(time_phrase)
            self.question_processed_form['time_phrase'] = time_phrase
        return self.question_processed_form

    def where_handler(self):
        return self.question_processed_form

    def why_handler(self):
        return self.question_processed_form

    def who_handler(self):
        #print('who')
        trees = self.get_processed_trees()
        for tree in trees:
            subject_phrase = tree_iterator(tree, 'SUBJECT_PHRASE').leaves()
            subject_phrase = ''.join(subject_phrase)
            self.question_processed_form['subject_phrase'] = subject_phrase
            time_phrase = tree_iterator(tree, 'TIME_PHRASE').leaves()
            time_phrase = ''.join(time_phrase)
            self.question_processed_form['time_phrase'] = time_phrase
            verb_phrase = tree_iterator(tree, 'VERB_PHRASE').leaves()
            verb_phrase = ''.join(verb_phrase)
            self.question_processed_form['verb_phrase'] = verb_phrase
        return self.question_processed_form

    def boolean_handler(self):
        #print('boolean')
        trees = self.get_processed_trees()
        for tree in trees:
            subject_phrase = tree_iterator(tree, 'SUBJECT_PHRASE').leaves()
            subject_phrase = ''.join(subject_phrase)
            self.question_processed_form['subject_phrase'] = subject_phrase
            try:
                time_phrase = tree_iterator(tree, 'TIME_PHRASE').leaves()
                time_phrase = ''.join(time_phrase)
                self.question_processed_form['time_phrase'] = time_phrase
            except AttributeError as ae:
                pass
            #verb_phrase = tree_iterator(tree, 'VERB_PHRASE').leaves()
            #verb_phrase = ''.join(verb_phrase)
            #self.question_processed_form['verb_phrase'] = verb_phrase
        return self.question_processed_form

    def quantity_handler(self):
        #print('quantity')
        trees = self.get_processed_trees()
        for tree in trees:
            subject_phrase = tree_iterator(tree, 'SUBJECT_PHRASE').leaves()
            subject_phrase = ''.join(subject_phrase)
            time = tree_iterator(tree, 'TIME_PHRASE').leaves()
            time = ''.join(time)
            self.question_processed_form['subject_phrase'] = subject_phrase
            self.question_processed_form['time_phrase'] = time
        return self.question_processed_form

    def other_handler(self):
        print('other')
        other_grammars = [('map.cfg', 'direction', 'LOCATION_NAME_TOTAL')]
        for grammar in other_grammars:
            trees = self.get_processed_trees(grammar=grammar[0])
            match_found = False
            for tree in trees:
                match_found = True
                subject_phrase = tree_iterator(tree, grammar[2]).leaves()
                subject_phrase = ''.join(subject_phrase)
                self.question_processed_form['subject_phrase'] = subject_phrase
                self.question_processed_form['category'] = grammar[1]

            if match_found:
                return self.question_processed_form

        if not match_found:
            self.question_processed_form['subject_phrase'] = 'Sorry ! we were not able to understand your question'
            return self.question_processed_form

    def get_processed_trees(self, grammar=None, trace= False):
        import os
        if not grammar:
            grammar_file = os.path.join(os.path.dirname(__file__), '../../grammars/generic_question', self.question.category)
        else:
            # do based on priority
            # do map first
            grammar_file = os.path.join(os.path.dirname(__file__), '../../grammars', grammar)
        with open(grammar_file, 'r') as file:
            grammar_str = file.read()
        grammar = nltk.PCFG.fromstring(grammar_str)
        parser = nltk.ViterbiParser(grammar)
        if trace: parser.trace()
        trees = parser.parse(self.question.question_extract)
        return trees

def understand(text):
    question = question_analyzer(text.strip().lower())
    analyzer = Analyzer(question)
    question_processed_form = analyzer.get_handler(question.category)()
    #print(question_processed_form)
    process_time_phrase(question_processed_form)
    return question_processed_form

def process_time_phrase(question_processed_form):
    # TODO: Support all time phrases
    import time
    import arrow
    if 'time_phrase' in question_processed_form:
        print(question_processed_form['time_phrase'])
        time_phrase = question_processed_form['time_phrase']
        if time_phrase.startswith('next'):
            exact_time = time_phrase.replace('next', '').strip()
            question_processed_form['time_phrase'] = process_time_word(exact_time, 1)
        elif time_phrase.startswith('last'):
            exact_time = time_phrase.replace('last', '').strip()
            question_processed_form['time_phrase'] = process_time_word(exact_time, -1)
        elif time_phrase.startswith('now'):
            now = arrow.now().strftime('%x %H:%M:%S')
            question_processed_form['time_phrase'] = now
        elif time_phrase.startswith('today'):
            today = time.strftime("%x")
            question_processed_form['time_phrase'] = today
        elif time_phrase.startswith('tomorrow'):
            time = arrow.now().shift(days=1)
            question_processed_form['time_phrase'] = time.datetime.strftime("%x")
        elif time_phrase.startswith('day after tomorrow'):
            time = arrow.now().shift(days=2)
            question_processed_form['time_phrase'] = time.datetime.strftime("%x")
        elif time_phrase.startswith('soon'):
            now = arrow.now().strftime('%H:%M:%S')
            future = arrow.now().shift(hours=4).strftime('%H:%M:%S')
            question_processed_form['time_phrase'] = now + '-' + future

def process_time_word(exact_time, indicator):
        import arrow
        timenow = arrow.now()
        if exact_time == 'week':
            if indicator == 1:
                time = timenow.shift(weeks=1)
                result = timenow.datetime.strftime("%x") + '-' + time.datetime.strftime("%x")
            elif indicator == -1:
                time = timenow.shift(weeks=-1)
                result = time.datetime.strftime("%x") + '-' + timenow.datetime.strftime("%x")
            return result

        elif exact_time == 'month':
            if indicator == 1:
                time = timenow.shift(months=1)
                result = timenow.datetime.strftime("%x") + '-' + time.datetime.strftime("%x")
            elif indicator == -1:
                time = timenow.shift(months=-1)
                result = time.datetime.strftime("%x") + '-' + timenow.datetime.strftime("%x")
            return result
        elif exact_time == 'year':
            if indicator == 1:
                time = timenow.shift(years=1)
                result = timenow.datetime.strftime("%x") + '-' + time.datetime.strftime("%x")
            elif indicator == -1:
                time = timenow.shift(years=-1)
                result = time.datetime.strftime("%x") + '-' + timenow.datetime.strftime("%x")
            return result
        '''
        elif exact_time == 'weekend':
            if indicator == 1:

            elif indicator == -1:
        elif exact_time == 'morning':
            if indicator == 1:

            elif indicator == -1:
        elif exact_time == 'afternoon':
            if indicator == 1:

            elif indicator == -1:

        elif exact_time == 'night':
            if indicator == 1:

            elif indicator == -1:
        '''

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

    if selected_category is None:
        selected_marker = 'other'
        selected_category = 'other'
        question_extract = text

    from collections import namedtuple
    Question = namedtuple('Question', ['category', 'marker_value', 'question_extract','actual_question'])
    question = Question(category=selected_category,
                        marker_value=selected_marker,
                        question_extract=question_extract,
                        actual_question=text)
    return question
