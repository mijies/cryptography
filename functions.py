
def lcm(a, b):
	return a * b // gcd(a, b)

def gcd(a, b):
	return b if a % b == 0 else gcd(b, a % b)

def minmum_coprime(a):
	for p in primes():
		if a % p != 0:
			return p

def primes(start=2, end=2**8+1):
	i = start if start % 2 != 0 else start + 1
	while True:
		if i > end: return
		for d in reversed(range(1, i)):
			if (i) % d == 0:
				break
		if d < 2: yield i
		i += 2

def extended_euclidean_algorithm(a, b):
	q = a // b
	r = a % b
	if r == 1:
		R = {r:1, b:0}
	else:
		R = extended_euclidean_algorithm(b, r)
	R[a]  = R[r] * a // a
	R[b] += R[r] * (-1) * b * q // b
	# print(R.keys(), R.values())
	return R
