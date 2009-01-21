import pysch
import pysch.atoms
import pysch.builtins
import pysch.atoms

# test builtin functions here

env = pysch.atoms.Environment(pysch.builtins.env)

def eval(str):
  return pysch.eval(pysch.read(str), env)

def test_add():
  assert eval('(+)')       == 0
  assert eval('(+ 2)')     == 2
  assert eval('(+ 2 3)')   == 5
  assert eval('(+ 2 3 4)') == 9
