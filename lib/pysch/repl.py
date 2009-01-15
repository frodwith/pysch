import pysch.reader as reader
import pysch.evaluator as evaluator
import pysch.builtins as builtins
import sys

def repl():
  while True:
    sys.stdout.write('pysch> ')
    sys.stdout.flush()
    line = sys.stdin.readline()

    if not line:
      return

    try:
      form = reader.read(line)
    except reader.ReadException as e:
      print('Syntax error:', e)
      continue

    try:
      result = evaluator.eval(form, builtins.env)
      print(result)
    except evaluator.EvaluationException as e:
      print('Evaluation error:', e)
      continue

if __name__ == '__main__':
  print('pysch lisp thingy -- Version 0.1')
  print('--------------------------------')
  repl()
