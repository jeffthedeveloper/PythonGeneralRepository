def my_generator():
  """Uma função geradora que retorna uma sequência de números quadrados."""

  i = 0
  while i < 10:
    i += 1
    n = i * i
    yield n


for n in my_generator():
  print(n)
