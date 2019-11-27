import sys
sys.path.append('..')
from functions import lcm, minmum_coprime, extended_euclidean_algorithm

class RSA:
	def __init__(self, p, q):
		self.p = p
		self.q = q
		self.N = p * q
		self.l = None # LCM of (p-1)*(q-1)
		self.e = None
		self.d = None
		self.i = None

	@property
	def params(self):
		print()
		print(' p: ', self.p)
		print(' q: ', self.q)
		print(' N: ', self.N)
		print(' l: ', self.l)
		print(' e: ', self.e)
		print(' d: ', self.d)
		print(' i: ', self.i)


	def calculate_params(self):
		self.l = lcm(self.p-1, self.q-1)
		self.e = minmum_coprime(self.l)

		a, b = (self.e, self.l) if self.e > self.l else (self.l, self.e)
		indef_dict = extended_euclidean_algorithm(a, b)
		self.d = indef_dict[self.e]
		self.i = indef_dict[self.l] * -1 # e*d - i*l = 1
		# print(indef_dict.keys(), indef_dict.values())

	def encrypt(self, m):
		if self.e is None:
			self.calculate_params()
		return m ** self.e % self.N

	def decrypt(self, c):
		if self.d is None:
			self.calculate_params()
		return c ** self.d % self.N

rsa = RSA(17, 19)
rsa.params
print(rsa.encrypt(65))
print(rsa.decrypt(12))
rsa.calculate_params()
rsa.params