import re
import pysch.atoms
import pysch

# use these instead of the bare strings so we don't confuse them for string
# literals, e.g. reader_symbol['.']
reader_symbols = {k: object() for k in ['(', ')', '.', "'", "`"]}
shorthand = {"'": 'quote', '`': 'quasiquote'}

class ReadException(pysch.Exception):
  pass

def read_literal(val):
  integer = re.match(r'^([+-])?(\d+)$', val)

  if integer:
    val = int(integer.group(2))
    if integer.group(1) == '-':
      val = -val

  elif val == '.':
    val = reader_symbols['.']

  else:
    val = pysch.atoms.get_symbol(val)

  return val

def tokenize(string):
  tokens = []
  current_token = ''
  quote_open = False 
  def end_token():
    nonlocal current_token

    if current_token:
      tokens.append(read_literal(current_token))

    current_token = ''
    
  for char in string:
    if quote_open:
      if char == '"':
        quote_open = False
        tokens.append(current_token)
        current_token = ''
      else:
        current_token += char

    elif char.isspace():
      end_token()
    elif char == '"':
      quote_open = True
    elif char in ['(', ')', '`', "'"]:
      end_token()
      tokens.append(reader_symbols[char])
    else: 
      current_token += char

  end_token()
  return tokens

def tree_to_cons(tree, i):
  length = len(tree)
  if i >= length:
    return pysch.atoms.nil

  item = tree[i]
  next = (i+1 < length) and tree[i+1]

  if next == reader_symbols['.']:
    if i+3 < length:
      raise ReadException('Too many items after dot')
    elif i+2 < length:
      return pysch.atoms.Cons(item, tree[i+2])
    else:
      raise ReadException('Dot with nothing following')

  for short in shorthand.keys():
    if item == reader_symbols[short]:
      if next:
        item = [pysch.atoms.get_symbol(shorthand[short]), next]
        del tree[i+1]
        break
      else:
        raise ReadException('"%s" with nothing following' % (short,))

  if type(item) == list:
    item = tree_to_cons(item, 0)

  return pysch.atoms.Cons(item, tree_to_cons(tree, i+1))

def read(string):
  tokens = tokenize(string)
  root   = []
  stack  = [root]

  for t in tokens:
    if t == reader_symbols['(']: 
      stack.append([])

    elif t == reader_symbols[')']:
      if len(stack) == 1:
        raise ReadException("Unmatched )")
      complete = stack.pop()
      stack[-1].append(complete)

    else:
      stack[-1].append(t)

  if len(stack) > 1:
    raise ReadException("Unmatched (")

  structure = tree_to_cons(root, 0)
  if (structure == pysch.atoms.nil):
    return None
  return structure.car
