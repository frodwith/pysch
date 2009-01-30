import pysch.evaluator
import pysch.atoms
from pysch.atoms import Cons

env = pysch.atoms.Environment()

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

@builtin()
def car(cons):
  return cons.car

@builtin()
def cdr(cons):
  return cons.cdr

@builtin('+')
def add(*args):
  sum = 0
  for n in args:
    sum += n
  return sum

@syntax('lambda')
def _lambda(args, env):
  arglist = args.car
  forms   = args.cdr

  return pysch.atoms.Lambda(env, arglist, forms)

@syntax('set!')
def _set(args, env):
  symbol = args.car
  val    = pysch.evaluator.eval(args.cadr, env)
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
    value  = pysch.evaluator.eval(args.cadr, env)

  env[symbol.string] = value
  return value

@syntax()
def quote(args, env):
  return args.car
