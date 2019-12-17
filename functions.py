import sympy

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
	while (i <= end):
		for d in reversed(range(i)):
			if i % d == 0:
				break
		if d < 2: yield i
		i += 2

def prime_factoring(n):
	
	# i = int(n**0.5) // 6 * 6 + 6
	# while i != 6:
	# 	if n % (i-1) == 0:
	# 		return i-1
	# 	if n % (i+1) == 0:
	# 		return i+1
	# 	i -= 6
	
	# if n % 2 == 0:
	# 	return 2
	# if n % 3 == 0:
	# 	return 3

	# check performance amoung use_trial, use_pm1 and use_rho
	return sympy.factorint(n).items().__iter__().__next__()[0]

	# i = int(n**0.5)
	# i = i if i % 2 != 0 else i - 1
	# while (n % i != 0):
	# 	i -= 2
	# return i

	# k = int(n**0.5)
	# i = 6
	# while i < k:
	# 	if n % (i-1) == 0:
	# 		return i-1
	# 	if n % (i+1) == 0:
	# 		return i+1
	# 	i += 6

def xgcd(a, b): # same as extended_euclidean_algorithm
	x, y,  u, v = 0, 1,  1, 0
	while b != 0:
		q = a // b
		r = a % b
		m = x - u * q
		n = y - v * q
		a,b, x,y, u,v = b,r, u,v, m,n
	return a, x, y

def extended_euclidean_algorithm(a, b): # same as xgcd
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
