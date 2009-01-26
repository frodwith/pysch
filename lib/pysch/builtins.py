import pysch.evaluator
from pysch.atoms import Syntax, Cons, Lambda, Environment, nil, get_symbol

# normal functions

def cons(car, cdr):
  return Cons(car, cdr)

def car(cons):
  return cons.car

def cdr(cons):
  return cons.cdr

def add(*args):
  sum = 0
  for n in args:
    sum += n
  return sum

# special forms

def _lambda(args, env):
  arglist = args.car
  forms   = args.cdr

  return Lambda(env, arglist, forms)

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

def quote(args, env):
  return args.car

# The Builtin Environment(tm)

env = Environment(initial = {
  '+':      add,
  'cons':   cons,
  'car':    car,
  'cdr':    cdr,
  'nil':    nil,

  'lambda': Syntax(_lambda),
  'quote' : Syntax(quote),
  'define': Syntax(define),
  'set!'  : Syntax(_set),
})
