import reader
import evaluator
import builtins
import sys

def repl():
  while True:
    print "pysch> ", 
    line = sys.stdin.readline()

    if not line:
      sys.exit(0)

    try:
      form = reader.read(line)
    except reader.ReadException, e:
      print "Syntax error:", e

    try:
      result = evaluator.eval(form, builtins.env)
      print result
    except evaluator.EvaluationException, e:
      print "Evaluation error:", e


if __name__ == '__main__':
  print "pysch lisp thingy -- Version 0.1"
  print "--------------------------------"
  repl()
