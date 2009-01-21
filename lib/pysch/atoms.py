import re
import pysch

class Nil:
  def __repr__(self):
    return '()'

  def __len__(self):
    return 0

  def __iter__(self):
    return self

  def __next__(self):
    raise StopIteration 

nil = Nil()

def is_cons(x):
  return hasattr(x, 'car') and hasattr(x, 'cdr')

class ConsIterator:
  def __init__(self, cons):
    self.cursor = cons
    self.proper = True

  def __iter__(self):
    return self

  def __next__(self):
    if self.cursor == nil:
      raise StopIteration

    if not is_cons(self.cursor):
      value = self.cursor
      self.cursor = nil
      self.proper = False
    else:
      value = self.cursor.car
      self.cursor = self.cursor.cdr

    return value

# a real linked list cell: iterable, indexable, and printable
class Cons:
  def __init__(self, car, cdr):
    self.car = car
    self.cdr = cdr

  def __iter__(self):
    return ConsIterator(self)

  def __getitem__(self, n):
    for val in self:
      if n == 0:
        return val
      n = n - 1

    raise IndexError('Index out of range')

  def __len__(self):
    l = 0
    for i in self:
      l = l + 1
    return l

  def __getattr__(self, key):
    match = re.match(r'^c([a|d]*)r$', key)
    if match:
      cursor = self
      for letter in match.group(1)[::-1]:
        if letter == 'a':
          cursor = cursor.car
        else:
          cursor = cursor.cdr
      return cursor

    raise AttributeError("'cons' object has no attribute '%s'" % (key,))

  def __repr__(self):
    list = iter(self)
    parts = [str(i) for i in list]
    if not list.proper:
      parts.insert(-1, '.')

    return '(' + ' '.join(parts) + ')'

class Environment(dict):
  def __init__(self, parent=None, initial=None):
    self.parent = parent
    if initial:
      self.update(initial)

  def __repr__(self):
    str = dict.__repr__(self)
    if self.parent:
      str += ' -> ' + self.parent.__repr__()

    return str

  def lookup(self, key):
    if key in self:
      return self[key]

    if self.parent:
      return self.parent.lookup(key)

    raise KeyError(key)

class Lambda:
  def __init__(self, env, args, forms):
    self.env   = env
    self.forms = forms
    self.args  = args

  def __repr__(self):
    return "<lambda\n  args:  %s\n  env:   %s\n  forms: %s>" \
      % (self.args, self.env, self.forms)

  def __call__(self, *args):
    env = Environment(self.env)
    env.update({b[0].string: b[1] for b in zip(self.args, args)})

    return [pysch.eval(f, env) for f in self.forms][-1]

class Syntax:
  def __init__(self, e):
    self.eval = e

def get_symbol(str):
  try:
    return Symbol.table[str]
  except KeyError:
    s = Symbol(str)
    Symbol.table[str] = s
    return s

class Symbol:
  table = {}

  def __init__(self, str):
    self.string = str

  def __repr__(self):
    return self.string
