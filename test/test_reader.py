from pysch import read
from pysch.atoms import nil

def test_ints():
  assert read('10') == 10
  assert read('1000000000') == 1000000000

def test_signed_ints():
  assert read('+20')  == 20
  assert read('-500') == -500

def test_nil():
  assert read('()') == nil

def test_pair():
  rep = '(foo . bar)'
  cons = read(rep)
  assert cons.car == 'foo'
  assert cons.cdr == 'bar'
  assert str(cons) == rep

def test_plain_list():
  rep = '(foo bar baz)'
  cons = read(rep)
  assert cons.car == 'foo'
  assert cons.cadr == 'bar'
  assert cons.caddr == 'baz'
  assert cons.cdddr == nil
  assert str(cons) == rep

def test_improper_list():
  rep = '(foo bar . baz)'
  cons = read(rep)
  assert cons.car == 'foo'
  assert cons.cadr == 'bar'
  assert cons.cddr == 'baz'
  assert str(cons) == rep

def test_quote_symbol():
  cons = read("'a")
  assert cons.car == 'quote'
  assert cons.cadr == 'a'
  assert cons.cddr == nil

def test_quote_list():
  cons = read("'(foo bar)")
  assert cons.car == 'quote'
  assert cons.caadr == 'foo'
  assert cons.cadadr == 'bar'
  assert cons.cddadr == nil
