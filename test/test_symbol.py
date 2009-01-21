from pysch.atoms import get_symbol, Symbol

def test_class():
  x = get_symbol('foo')
  assert type(x) == Symbol

def test_equality():
  x = get_symbol('foo')
  y = get_symbol('foo')
  assert x == y

def test_value():
  x = get_symbol('foo')
  assert x.string == 'foo'

def test_inequality():
  x = get_symbol('foo')
  y = get_symbol('bar')
  assert x != y
