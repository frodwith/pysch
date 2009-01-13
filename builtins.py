import pysch.atoms

def add(*args):
  sum = 0
  for n in args:
    sum += n
  return sum

env = {
  '+':   add,
  'nil': pysch.atoms.nil
}

env = pysch.atoms.Environment(None, **env)
