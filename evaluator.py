import types;

py_apply = apply

class EvaluationException(Exception):
  pass

class UnboundException(EvaluationException):
  pass

def apply(fn, args):
  if type(fn) == types.FunctionType: 
    return py_apply(fn, args)

  raise EvaluationException, "User-defined functions not yet implemented"

def eval(expr, env):
  if type(expr) == list:
    if len(expr) < 1:
      return expr

    values = [eval(e,env) for e in expr]
    return apply(values[0], values[1:])

  if type(expr) == types.IntType:
    return expr

  try:
    return env[expr]
  except KeyError:
    raise UnboundException, "'%s' is not bound" % (expr, )
