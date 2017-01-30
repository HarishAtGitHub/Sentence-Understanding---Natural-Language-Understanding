import nltk

with open('../grammars/map.cfg', 'r') as file:
    grammar_str = file.read()

def validate(text):
  grammar = nltk.PCFG.fromstring(grammar_str)
  parser = nltk.ViterbiParser(grammar)
  trees = parser.parse(list(text))
  valid = False
  location_name = None
  for tree in trees:
    value = tree_iterator(tree).leaves()
    location_name = ''.join(value)
    valid = True
  return (valid,location_name)

def tree_iterator(tree):
  value = None
  for a in tree:
     if isinstance(a, str):
         continue
     if a.label() == 'LOCATION_NAME_TOTAL':
         value = a
         break
     else:
         temp = tree_iterator(a)
         if temp is not None:
             value = temp
  return value

def assist(text):
    input_tokens = text.split(' ')
    direction_keywords = ['where', 'path', 'directions', 'direction']
    for keyword in direction_keywords:
        if keyword in input_tokens:
            print(' Are you searching for a place ?')

def print_validity(text, state, marker = None):
    if marker is not None:
        text = 'Input text: ' + text + ' --> ' + marker + ' ' + state + ' direction question '
    else:
        text = 'Input text: ' + text + ' --> ' + state + ' direction question '
    print(text)

lines = [line.rstrip('\n') for line in open('../test/inputs/map')]

for line in lines:
    print('##################################################################')
    print()
    invalid_marker = '??????????'
    try:
        result = validate(line)
        if result[0]:
            print_validity(line, 'Valid')
            print(' { \n "query type": "direction" , \n "params" : { \n"location_name" :   "' + result[1] + '"  \n} \n}')
        else:
            print_validity(line, 'Invalid', invalid_marker)
            assist(line)
    except ValueError as ve:
        print(ve)
        print_validity(line, 'Invalid', invalid_marker)
        assist(line)
        continue