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

def test_quasiquote():
  qq = eval('(quasiquote (3 (4 (unquote (+ 2 3)))))')
  print(qq)
  assert qq.car == 3
  assert qq.caadr == 4
  assert qq.cadadr == 5
