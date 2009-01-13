def tokenize(string):
  tokens = []
  current_token = ''

  def end_token():
    if current_token:
      tokens.append(current_token)
    return ''
    
  for char in string:
    if char.isspace():
      current_token = end_token()
    elif char == '(' or char == ')':
      current_token = end_token()
      tokens.append(char)
    else:
      current_token += char

  return tokens

def read(string):
  tokens = tokenize(string)
  root = []
  stack = [root]

  for t in tokens:
    if t == '(': 
      stack.append([])

    elif t == ')':
      if len(stack) > 1:
        complete = stack.pop()
        stack[-1].append(complete)
      else:
        raise Exception, "Unmatched )"

    else:
      stack[-1].append(t)

  if len(stack) > 1:
    raise Exception, "Unmatched ("

  return root

if __name__ == '__main__':
  import sys
  slurp = sys.stdin.read()
  print read(slurp)
