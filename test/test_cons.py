from pysch.atoms import Cons, nil
import nose.tools

proper = Cons(1, Cons(2, Cons(3, nil)))
improper = Cons(1, Cons(2, 3))

def test_cons():
  cons = Cons(1,2)
  assert cons.car == 1
  assert cons.cdr == 2

def assert_list_eq(expected, got):
  l = len(expected)
  assert l == len(got) 
  for i in range(l):
    assert expected[i] == got[i]

def test_iteration():
  comp = [i for i in proper]
  assert_list_eq(proper, comp)

def test_improper_iteration():
  it = iter(improper)
  items = []
  for i in it:
    items.append(i)

  assert_list_eq([1,2,3], items)
  assert not it.proper

def listiness(l):
  assert_list_eq([1,2,3], l)
  nose.tools.assert_raises(IndexError, l.__getitem__, 4)

def test_listy():
  listiness(proper)

def test_improper_listy():
  listiness(improper)

def test_stringify():
  assert str(proper) == '(1 2 3)'
  assert str(improper) == '(1 2 . 3)'
  assert str(Cons(1, 2)) == '(1 . 2)'

def test_cadr_chain():
  assert proper.car == 1
  assert proper.cadr == 2
  assert proper.caddr == 3
  assert improper.cddr == 3
