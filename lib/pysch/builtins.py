import pysch.evaluator
import pysch.atoms
from pysch.atoms import Cons

env = pysch.atoms.Environment()

env['eval'] = pysch.eval
env['nil'] = pysch.atoms.nil

def builtin(name=None):
  def deco(fn):
    n = name or fn.__name__
    env[n] = fn
    return fn

  return deco

def syntax(name=None):
  def deco(fn):
    n = name or fn.__name__
    env[n] = pysch.atoms.Syntax(fn)
    return fn

  return deco

@builtin()
def cons(car, cdr):
  return Cons(car, cdr)

@builtin('+')
def add(*args):
  sum = 0
  for n in args:
    sum += n
  return sum

@builtin('eq?')
def eq(x, y):
  return x == y

@builtin('pair?')
def pairp(x):
  return type(x) == Cons

def _repr(x):
  if (x == True):
    return '#t'
  elif (x == False):
    return '#f'
  else:
    return repr(x)

@builtin('print')
def _print(*args):
  for i in args:
    print(_repr(i))

@syntax('syntax')
def _syntax(args, env):
  fn = pysch.eval(args.car, env)
  return pysch.atoms.Syntax(fn)

@syntax('lambda')
def _lambda(args, env):
  arglist = args.car
  forms   = args.cdr

  return pysch.atoms.Lambda(env, arglist, forms)

@syntax('set!')
def _set(args, env):
  symbol = args.car
  val    = pysch.eval(args.cadr, env)
  name   = symbol.string

  # find where the thing is bound
  while not name in env: 
    if not env.parent:
      raise pysch.evaluator.UnboundException(
        "Cannot set! unbound variable '%s'" % (name, ))
    env = env.parent

  # change its binding
  env[name] = val
  return val

@syntax()
def define(args, env):
  if(type(args.car) == Cons):
    symbol = args.caar
    args = Cons(args.cdar, args.cdr)
    value = _lambda(args, env)
  else:
    symbol = args.car
    value  = pysch.eval(args.cadr, env)

  env[symbol.string] = value
  return value

@syntax()
def quote(args, env):
  return args.car

@syntax('if')
def _if(args, env):
  condition = pysch.eval(args.car, env)
  if len(args) != 3:
    msg = 'if called with %d args: %s' % (len(args), args.car)
    raise pysch.evaluator.EvaluationException(msg)
      

  if condition:
    e = args.cadr
  else:
    e = args.caddr

  return pysch.eval(e, env)

def read_prelude():
  prelude = open('prelude.scm', 'r')
  source = '(' + prelude.read() + ')'
  toplevel = pysch.read(source)
  for form in toplevel:
    pysch.eval(form, env)

read_prelude()
