class Nil:
  def __repr__(self):
    return '()'

nil = Nil()

def is_cons(x):
  return hasattr(x, 'car') and hasattr(x, 'cdr')

class ConsIterator():
  def __init__(self, cons):
    self.cursor = cons
    self.proper = True

  def __iter__(self):
    return self

  def next(self):
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
class Cons():
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

    raise IndexError, 'Index out of range'

  def __repr__(self):
    iter = self.__iter__()
    parts = [str(i) for i in iter]
    if not iter.proper:
      parts.insert(-1, '.')

    return '(' + ' '.join(parts) + ')'

def list_to_cons(list):
  length = len(list)

  def builder(n):
    if n == length:
      return nil

    return Cons(list[n], builder(n+1))

  return builder(0)

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
    except KeyError, e:
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

    for i in xrange(0, len(self.args)):
      var = self.args[i]
      env[var] = args[i]

    last_value = None
    for f in self.forms:
      last_value = pysch.evaluator.eval(f, env)

    return last_value
