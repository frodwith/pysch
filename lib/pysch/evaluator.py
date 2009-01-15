import types
import pysch.atoms

class EvaluationException(Exception):
  pass

class UnboundException(EvaluationException):
  pass

def eval_lambda(expr, env):
  iter  = expr.cdr
  args  = iter.car
  forms = iter.cdr

  return pysch.atoms.Lambda(env, args, forms)

def eval_define(expr, env):
  iter = expr.cdr
  name = iter.car

  iter = iter.cdr
  val  = eval(iter.car, env)

  env[name] = val
  return val

def eval_quote(expr, env):
  return expr.cdr.car

special_forms = {
  'lambda': eval_lambda,
  'define': eval_define,
  'quote' : eval_quote,
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
    return env[expr]
  except KeyError:
    raise UnboundException("'%s' is not bound" % (expr, ))
