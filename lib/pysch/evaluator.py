import types
import pysch.atoms
import pysch

class EvaluationException(pysch.Exception):
  pass

class UnboundException(EvaluationException):
  pass

def eval_form(expr, env):
  op   = eval(expr.car, env)
  args = expr.cdr

  if type(op) == pysch.atoms.Syntax:
    return op.eval(args, env)
  else:
    args = [eval(a, env) for a in args]
    try:
      return op(*args)
    except TypeError as e:
      raise EvaluationException('Operator is not callable') from e

def eval(expr, env):
  if type(expr) == int:
    return expr

  if expr == pysch.atoms.nil:
    return expr

  if type(expr) == pysch.atoms.Symbol:
    sym = expr.string
    try:
      return env.lookup(sym)
    except KeyError as e:
      raise UnboundException("'%s' is not bound" % (sym, )) from e

  if pysch.atoms.is_cons(expr):
    return eval_form(expr, env)

  raise EvaluationException('Tried to evaluate a value of unknown type')
