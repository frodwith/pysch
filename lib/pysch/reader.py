import re
import pysch.atoms
import pysch

class ReadException(pysch.Exception):
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

quote_marker = object()
dot_marker = object()

def tree_to_cons(tree, i):
  length = len(tree)
  if i >= length:
    return pysch.atoms.nil

  item = tree[i]
  next = (i+1 < length) and tree[i+1]

  if (next == dot_marker):
    if i+3 < length:
      raise ReadException('Too many items after dot')
    elif i+2 < length:
      return pysch.atoms.Cons(item, tree[i+2])
    else:
      raise ReadException('Dot with nothing following')

  if item == quote_marker:
    if next:
      item = ['quote', next]
      del tree[i+1]
    else:
      raise ReadException('Quote with nothing following')

  if type(item) == list:
    item = tree_to_cons(item, 0)

  return pysch.atoms.Cons(item, tree_to_cons(tree, i+1))

def read(string):
  tokens = tokenize(string)
  root   = []
  stack  = [root]

  for t in tokens:
    if t == '(': 
      stack.append([])

    elif t == ')':
      if len(stack) == 1:
        raise ReadException("Unmatched )")
      complete = stack.pop()
      stack[-1].append(complete)

    elif t == '.':      
      stack[-1].append(dot_marker)

    elif t == "'":
      stack[-1].append(quote_marker)

    else:
      match = re.match(r'^([+-])?(\d+)$', t)
      if match:
        t = int(match.group(2))
        if match.group(1) == '-':
          t = -t

      stack[-1].append(t)

  if len(stack) > 1:
    raise ReadException("Unmatched (")

  return tree_to_cons(root, 0).car
