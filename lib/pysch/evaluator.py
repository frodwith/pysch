import types
import pysch.atoms
import pysch

class EvaluationException(pysch.Exception):
  pass

class UnboundException(EvaluationException):
  pass

def eval_lambda(expr, env):
  expr  = expr.cdr
  args  = expr.car
  forms = expr.cdr

  return pysch.atoms.Lambda(env, args, forms)

def eval_set(expr, env):
  expr = expr.cdr
  name = expr.car
  val = eval(expr.cadr, env)

  # find where the thing is bound
  while not name in env: 
    if not env.parent:
      raise UnboundException("Cannot set! unbound variable '%s'" % (name, ))
    env = env.parent

  # change its binding
  env[name] = val
  return val

def eval_define(expr, env):
  name = expr.cadr
  
  # establish a binding at this level
  env[name] = None

  # and set its value
  return eval_set(expr, env)

def eval_quote(expr, env):
  return expr.cdr.car

special_forms = {
  'lambda': eval_lambda,
  'quote' : eval_quote,
  'define': eval_define,
  'set!'  : eval_set,
}

def eval_form(expr, env):
  try:
    return special_forms[expr.car](expr, env)
  except KeyError:
    values = [eval(e,env) for e in expr]
    return values[0](*values[1:])

def eval(expr, env):
  if type(expr) == int:
    return expr

  if expr == pysch.atoms.nil:
    return expr

  if pysch.atoms.is_cons(expr):
    return eval_form(expr, env)

  try:
    return env.lookup(expr)
  except KeyError:
    raise UnboundException("'%s' is not bound" % (expr, ))
