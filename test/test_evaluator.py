import pysch
import pysch.evaluator
import pysch.builtins
import pysch.atoms
import nose.tools

# Test special forms here, as well

env = None

def eval(str):
  form = pysch.read(str)
  return pysch.eval(form, env)

def setup():
  global env
  env = pysch.atoms.Environment(pysch.builtins.env)

def test_literals():
  assert eval('"foo bar"') == 'foo bar'
  assert eval('1') == 1
  assert eval('()') == pysch.atoms.nil

def test_define():
  eval('(define x 1)')
  assert eval('x') == 1

def test_lambda():
  assert eval('((lambda () 1))') == 1
  assert eval('((lambda (x) x) 1)') == 1
  assert eval('((lambda (x y) (+ x y)) 3 5)') == 8
  assert eval('(((lambda (x) (lambda (y) (+ x y))) 2) 3)') == 5

def test_set():
  eval('(define x 10)')
  eval('(set! x 5)')

  assert eval('x') == 5

  nose.tools.assert_raises(pysch.evaluator.UnboundException,
    eval, '(set! y 10)')

def test_closure():
  eval('(define x 10)')
  eval('(define reader (lambda () x))')
  eval('(define writer (lambda (y) (set! x y)))')
  assert eval('(reader)') == 10
  eval('(writer 5)')
  assert eval('(reader)') == 5
