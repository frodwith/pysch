import types
import pysch.atoms

class EvaluationException(Exception):
  pass

class UnboundException(EvaluationException):
  pass

def eval(expr, env):
  if type(expr) == list:
    if len(expr) < 1:
      return pysch.atoms.nil

    if expr[0] == 'lambda':
      return pysch.atoms.Lambda(
        env = env,
        args = expr[1],
        forms = expr[2:],
      )

    if expr[0] == 'define':
      name = expr[1]
      val  = eval(expr[2], env)
      env[name] = val
      return val

    values = [eval(e,env) for e in expr]
    return apply(values[0], values[1:])

  if type(expr) == types.IntType:
    return expr

  try:
    return env[expr]
  except KeyError:
    raise UnboundException, "'%s' is not bound" % (expr, )
