nil = []

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
