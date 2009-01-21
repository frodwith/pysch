from pysch import read
from pysch.atoms import nil, Symbol, get_symbol

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
  assert cons.car == get_symbol('foo')
  assert cons.cdr == get_symbol('bar')
  assert str(cons) == rep

def test_plain_list():
  rep = '(foo bar baz)'
  cons = read(rep)
  assert cons.car == get_symbol('foo')
  assert cons.cadr == get_symbol('bar')
  assert cons.caddr == get_symbol('baz')
  assert cons.cdddr == nil
  assert str(cons) == rep

def test_improper_list():
  rep = '(foo bar . baz)'
  cons = read(rep)
  assert cons.car == get_symbol('foo')
  assert cons.cadr == get_symbol('bar')
  assert cons.cddr == get_symbol('baz')
  assert str(cons) == rep

def test_quote_symbol():
  cons = read("'a")
  assert cons.car == get_symbol('quote')
  assert cons.cadr == get_symbol('a')
  assert cons.cddr == nil

def test_quote_list():
  cons = read("'(foo bar)")
  assert cons.car == get_symbol('quote')
  assert cons.caadr == get_symbol('foo')
  assert cons.cadadr == get_symbol('bar')
  assert cons.cddadr == nil

def test_nested_lists():
  cons = read('((foo) (bar baz) (qux (quux) quuux) thud (splat))')
  assert cons.caar == get_symbol('foo')
  assert cons.caadr == get_symbol('bar')
  assert cons.cadadr == get_symbol('baz')
  assert cons.caaddr == get_symbol('qux')
  assert cons.caadaddr == get_symbol('quux')
  assert cons.caddaddr == get_symbol('quuux')
  assert cons.cadddr == get_symbol('thud')
  assert cons.caaddddr == get_symbol('splat')
