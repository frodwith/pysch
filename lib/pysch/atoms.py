import re

class Nil:
  def __repr__(self):
    return '()'

  def __len__(self):
    return 0

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

    raise AttributeException("'cons' object has no attribute '%s'" % (key,))

  def __repr__(self):
    list = iter(self)
    parts = [str(i) for i in list]
    if not list.proper:
      parts.insert(-1, '.')

    return '(' + ' '.join(parts) + ')'

class Environment(dict):
  def __init__(self, parent=None, **kwargs):
    self.parent = parent
    self.update(kwargs)

  def __repr__(self):
    str = dict.__repr__(self)
    if self.parent:
      str += ' -> ' + self.parent.__repr__()

    return str

  def __getitem__(self, key):
    try:
      return dict.__getitem__(self, key)
    except KeyError as e:
      if self.parent:
        return self.parent[key]
      raise e

class Lambda:
  def __init__(self, env, args, forms):
    self.env   = env
    self.forms = forms
    self.args  = args

  def __repr__(self):
    return "<lambda\n  args:  %s\n  env:   %s\n  forms: %s>" \
      % (self.args, self.env, self.forms)

  def __call__(self, *args):
    import pysch.evaluator

    env = Environment()
    env.parent = self.env

    for i in range(0, len(self.args)):
      var = self.args[i]
      env[var] = args[i]

    last_value = None
    for f in self.forms:
      last_value = pysch.evaluator.eval(f, env)

    return last_value
