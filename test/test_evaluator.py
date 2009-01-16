import pysch
import pysch.atoms as atoms

env = None

def eval(str):
  form = pysch.read(str)
  return pysch.eval(form, env)

def setup():
  global env
  env = atoms.Environment()

def test_define():
  eval('(define x 1)')
  assert eval('x') == 1
