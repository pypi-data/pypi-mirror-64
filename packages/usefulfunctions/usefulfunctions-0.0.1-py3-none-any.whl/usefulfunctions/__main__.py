def average(params):
  return sum(params, 0.0) / len(params)

def bytes(string):
  return len(s.encode('utf-8'))


def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


def divisible(dividend, divisor):
  if dividend % divisor == 0:
    return True
  else:
    return False

def fib(n):
  if n <= 0:
    return [0]
  sequence = [0, 1]
  while len(sequence) <= n:
    next_value = sequence[len(sequence) - 1] + sequence[len(sequence) - 2]
    sequence.append(next_value)
  return sequence

def isprime(x):
    if x <= 1:
        return False
    if x <= 3:
        return True
    i = 7
    while i ** 2:
        if x % 2 == 0 or x % 3 == 0 or x % 5 == 0:
            return False
        if x % i == 0:
            return False
        i += 2
    return True

def primeFactors(n):
    while n % 2 == 0:
        print(2),
        n = n / 2
    for i in range(3,int(math.sqrt(n))+1,2):
        while n % i== 0:
            print(i),
            n = n / i
    if n > 2:
        print(n)

def reverse(str):
  return str[::-1]


def similarity(a, b):
  return [item for item in a if item in b]
