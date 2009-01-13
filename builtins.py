def add(*args):
  sum = 0
  for n in args:
    sum += n
  return sum

env = {
  '+': add 
}
