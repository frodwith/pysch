import pysch.atoms

def cons(car, cdr):
  return pysch.atoms.Cons(car, cdr)

def car(cons):
  return cons.car

def cdr(cons):
  return cons.cdr

def add(*args):
  sum = 0
  for n in args:
    sum += n
  return sum

env = {
  '+':    add,
  'cons': cons,
  'car':  car,
  'cdr':  cdr,
  'nil':  pysch.atoms.nil
}
env = pysch.atoms.Environment(None, **env)
