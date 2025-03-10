function encrypt(m, len):
  res = [0]*len # this variable is set to [0, 0, ..., 0] where the array has length len
  for i = 0,1,...,len-1:
    res[i] = chr((ord(m[i]) * ord(m[(i+1)%len])) % 26)
  return res

Where ord is the function that maps A to 0, B to 1 and so on, while chr is its inverse function. How many strings m (even meaningless) are there such that encrypt(m, 10) = "BBBBBBBBBB"?

2
13
26
1
