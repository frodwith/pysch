import pysch

class EvaluationException(pysch.Exception):
  pass

class UnboundException(EvaluationException):
  pass

def eval(expr, env):
  import pysch.atoms as atom
  def literal():
    return expr

  def symbol():
    sym = expr.string
    try:
      return env.lookup(sym)
    except KeyError as e:
      raise UnboundException("'%s' is not bound" % (sym, )) from e

  def form():
    op   = eval(expr.car, env)
    args = expr.cdr

    if type(op) == atom.Syntax:
      return op.eval(args, env)
    else:
      args = [eval(a, env) for a in args]
      try:
        return op(*args)
      except TypeError as e:
        raise EvaluationException('Operator is not callable') from e

  try:
    return {
      atom.Symbol: symbol,
      atom.Cons:   form,
      atom.Nil:    literal,
      str:         literal,
      int:         literal,
    }[type(expr)]()
  except KeyError as e:
    raise EvaluationException(
      'Tried to evaluate a value of unknown type') from e
