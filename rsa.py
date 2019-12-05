import math
import os
import re
import subprocess
import sys
sys.path.append('..')
from functions import lcm, minmum_coprime, prime_factoring, extended_euclidean_algorithm


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
		print(' (p)prime1:\t\t', self.p)
		print(' (q)prime2:\t\t', self.q)
		print(' (N)modulus:\t\t', self.N)
		print(' (l)LCM:\t\t', self.l)
		print(' (e)publicExponent:\t', self.e)
		print(' (d)privateExponent:\t', self.d)
		print(' (i):\t', self.i)

	@property
	def pubkey(self):
		if not hasattr(self, '_pubkey'):
			print('\n public key is not set')
		else:
			print('\n public key : ', self._pubkey)
			print(' bit length : ', self.key_bit)
			print(' modulus(N) : ', self.modulus)
			print(' exponent(e): ', self.exponent)
		

	def calculate_params(self, e=None):
		self.l = lcm(self.p-1, self.q-1)
		self.e = e if e is not None else minmum_coprime(self.l)

		phi = (self.p-1) * (self.q-1)
		# phi = self.l
		a, b = (self.e, phi) if self.e > phi else (phi, self.e)
		indef_dict = extended_euclidean_algorithm(a, b)

		# make indef_dict[self.e] the minimum positive integer if negative
		# Bézout's identity => a(x + bn) + b(y + an) = 1
		while indef_dict[self.e] < 0:
			indef_dict[self.e] += phi
			indef_dict[phi] += 1

		self.d = indef_dict[self.e]
		self.i = indef_dict[phi] * -1 # e*d - i*phi = 1 => e*d = i*(p-1)(q-1) + 1
		print(indef_dict.keys(), indef_dict.values())


	def encrypt(self, m):
		if self.e is None:
			self.calculate_params()
		return m ** self.e % self.N

	def decrypt(self, c):
		if self.d is None:
			self.calculate_params()
		return c ** self.d % self.N


	def load_public_key(self, file_path):
		if '/' in file_path:
			file_path = file_path.replace('/', os.sep)

		if not os.path.exists(file_path):
			raise IOError(file_path + ': No such file')

		cmd = "openssl rsa -text -noout -pubin -in " + file_path
		output = subprocess.check_output(cmd.split()).decode('utf-8')

		pattern = '.*Modulus: (\d+).*'
		result  = re.match(pattern, output, re.S)
		if result is None:
			print('Could not parse:' + file_path)
			return
		else:
			self.modulus = int(result.group(1))

		pattern = '.*Exponent: (\d+).*'
		result  = re.match(pattern, output, re.S)
		if result is None:
			print('Could not parse:' + file_path)
			return
		else:
			self.exponent = int(result.group(1))

		self.key_bit = math.ceil(math.log(self.modulus, 2))
		self._pubkey = file_path

	
	def update_params_by_pubkey(self):
		if not hasattr(self, '_pubkey'):
			print('\n public key is not set')
			return

		if self.key_bit > 64:
			print('\n key length is ' + str(self.key_bit))
			print('\n computation may take a substantial time')

		n = self.modulus
		self.p = prime_factoring(n)
		self.q = n // self.p
		self.N = n
		self.calculate_params(e=self.exponent)


	def generate_private_key(self):
		if not hasattr(self, '_pubkey'):
			print('\n public key is not set')
			return
		
		if self.N != self.modulus:
			print('\n updating params by public key')
			self.update_params_by_pubkey()

		file_asn = 'asn1parse.txt'
		file_pri = 'fake.key'
		file_pem = 'fake.pem'

		txt  = 'asn1=SEQUENCE:rsa_key\n\n[rsa_key]\nversion=INTEGER:0'
		txt += '\nmodulus=INTEGER:' + str(self.N)
		txt += '\npubExp=INTEGER:' + str(self.e)
		txt += '\nprivExp=INTEGER:' + str(self.d)
		txt += '\np=INTEGER:' + str(self.p)
		txt += '\nq=INTEGER:' + str(self.q)
		txt += '\ne1=INTEGER:' + str(self.d % (self.p-1))
		txt += '\ne2=INTEGER:' + str(self.d % (self.q-1))
		txt += '\ncoeff=INTEGER:' + str(pow(self.q, self.p-2, self.p))
		txt += '\n'
		
		with open(file_asn, 'w') as f:
			f.write(txt)

		cmd  = "openssl asn1parse -genconf " + file_asn
		cmd += " -out " + file_pri
		output = subprocess.check_output(cmd.split()).decode('utf-8')
		print('\n generated ', file_pri)
		print(output)

		cmd  = "openssl rsa -inform der -outform pem -in " + file_pri
		cmd += " -out " + file_pem
		output = subprocess.check_output(cmd.split()).decode('utf-8')
		print('\n generated ', file_pem)
		print(output)

	
	def print_private_key(self, file_path):
		if '/' in file_path:
			file_path = file_path.replace('/', os.sep)

		if not os.path.exists(file_path):
			raise IOError(file_path + ': No such file')

		cmd = "openssl rsa -text -noout -in " + file_path
		output = subprocess.check_output(cmd.split()).decode('utf-8')
		print('\n', output)