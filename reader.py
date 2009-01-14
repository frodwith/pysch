import re
import pysch.atoms

class ReadException(Exception):
  pass

def tokenize(string):
  tokens = []
  current_token = ''

  def end_token():
    if current_token:
      tokens.append(current_token)
    return ''
    
  for char in string:
    if char.isspace():
      current_token = end_token()
    elif char == '(' or char == ')':
      current_token = end_token()
      tokens.append(char)
    else: 
      current_token += char

  return tokens

integer = re.compile(r'^\d+$')

def read(string, multiple=False):
  tokens = tokenize(string)
  root = []
  stack = [root]

  for t in tokens:
    if t == '(': 
      stack.append([])

    elif t == ')':
      if len(stack) > 1:
        complete = stack.pop()
        stack[-1].append(pysch.atoms.list_to_cons(complete))
      else:
        raise ReadException, "Unmatched )"

    else:
      if (re.match(integer, t)):
        t = int(t)

      stack[-1].append(t)

  if len(stack) > 1:
    raise ReadException, "Unmatched ("

  if multiple:
    return root
  else:
    return root[-1]
