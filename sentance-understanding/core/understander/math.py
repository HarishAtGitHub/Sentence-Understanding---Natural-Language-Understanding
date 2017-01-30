import nltk

PLUS = 'plus'
MUL = 'multiplied by'
DIV = 'divided by'
MIN = 'minus'
OPENB = 'open bracket'
CLOSEB = 'close bracket'

with open('../grammars/math.cfg', 'r') as file:
    grammar_str = file.read()

def validate(text):
  grammar = nltk.CFG.fromstring(grammar_str)
  parser = nltk.ChartParser(grammar)
  trees = parser.parse(list(text))
  valid = False
  answer = math_form = None
  for tree in trees:
    addition = tree[4].leaves()
    operation_string = ''
    for i in addition:
        operation_string = operation_string + i
    p = operation_string.replace(PLUS, '+')\
        .replace(MUL, '*') \
        .replace(DIV, '/') \
        .replace(MIN, '-') \
        .replace(OPENB, '(') \
        .replace(CLOSEB, ')')
    math_form= p
    answer = eval(p)
    valid = True
    break
  return (valid, math_form, answer)

def print_validity(text, state, marker = None):
    if marker is not None:
        text = 'Input text: ' + text + ' --> ' + marker + ' ' + state + ' Math question '
    else:
        text = 'Input text: ' + text + ' --> ' + state + ' Math question '
    print(text)

lines = [line.rstrip('\n') for line in open('../test/inputs/math')]

for line in lines:
    print('##################################################################\n')
    invalid_marker = '??????????'
    try:
      result = validate(line)
      if result[0]:
          print_validity(line, "Valid")
          print(' math form : ' + result[1])
          print(' answer : ' + str(result[2]))
      else:
          print_validity(line, "Invalid", invalid_marker)
    except ValueError as ve:
      print(ve)
      print_validity(line, "Invalid", invalid_marker)
      continue
