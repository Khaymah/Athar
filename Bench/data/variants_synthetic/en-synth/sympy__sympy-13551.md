Product(n + 1 / 2**k, [k, 0, n-1]).doit() gives back a wrong closed form. here's what I get (simplified result + the value at n=2):
[[A1]]
for n=2 it should be (2 + 2^0) * (2 + 2^(-1)) = 15/2. fwiw I think the correct expression involves the q-Pochhammer symbol: https://www.wolframalpha.com/input/?i=product+of+n+%2B+1%2F2%5Ek+from+k%3D0+to+n-1
