import struct
import sys
import time
# sys.path.append('.')
from rsa import RSA


rsa = RSA(17, 19)
rsa.params
rsa.calculate_params()
rsa.params

msg = struct.unpack('>B', 'A'.encode())[0]
print(msg)
print(rsa.encrypt(msg))
print(rsa.decrypt(rsa.encrypt(msg)))
print(struct.pack('>B', rsa.decrypt(rsa.encrypt(msg))).decode('utf-8'))


# rsa.load_public_key('data/public.key')
rsa = RSA('data/public.key')
rsa.pubkey
rsa.update_params_by_pubkey()
rsa.params
rsa.generate_private_key()

rsa.print_private_key('data/private.key')
rsa.print_private_key('fake.pem')

print(msg)
print(rsa.encrypt(msg))
print(rsa.decrypt(rsa.encrypt(msg)))

from functions import prime_factoring
start_time = time.time()
# prime_factoring(3092753269)
prime_factoring(12814570762777948741)
print(time.time() - start_time)



# start_time = time.time()
# print(pow(15,3000351,51077))
# print(time.time() - start_time)

# start_time = time.time()
# print(15**3000351%51077)
# print(time.time() - start_time)
