import sys
import string
import random
import hashlib


password = sys.argv[1]

salt = ''.join(random.sample(string.ascii_letters, 20))
print salt


for i in range(3):
    password = salt.join(password)
    password = str(hashlib.sha1(password).hexdigest())
print salt + password 
