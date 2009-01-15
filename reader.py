import re
import pysch.atoms

class ReadException(Exception):
  pass

def tokenize(string):
  tokens = []
  current_token = ''

  def end_token():
    nonlocal current_token
    if current_token:
      tokens.append(current_token)
    current_token = ''
    
  for char in string:
    if char.isspace():
      end_token()
    elif char in ['(', ')', "'"]:
      end_token()
      tokens.append(char)
    else: 
      current_token += char

  end_token()
  return tokens

integer = re.compile(r'^\d+$')

def tree_to_cons(tree, i):
  try:
    item = tree[i]
  except IndexError:
    return pysch.atoms.nil

  if type(item) == list:
    item = tree_to_cons(item, 0)

  return pysch.atoms.Cons(item, tree_to_cons(tree, i+1))

def read(string, multiple=False):
  tokens = tokenize(string)
  root   = []
  stack  = [root]

  def add(item):
    top = stack[-1]
    top.append(item)
    if top[0] == "'":
      top[0] = 'quote'
      add(stack.pop())

  for t in tokens:
    if t == '(': 
      stack.append([])

    elif t == ')':
      if len(stack) == 1:
        raise ReadException("Unmatched )")
      add(stack.pop())

    elif t == "'":
      stack.append(["'"])

    else:
      if (re.match(integer, t)):
        t = int(t)
      add(t)

  if len(stack) > 1:
    raise ReadException("Unmatched (")

  return tree_to_cons(root, 0).car
