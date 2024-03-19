import bcrypt

def hash_password(password):
   password_bytes = password.encode('utf-8')
   hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
   return hashed_bytes.decode('utf-8')

s = '$2b$12$FP0EeppGwH/dQ32LH5Z58.4eDnbef.pNSZBf1JJV4XirKzZtZR5/O'

print(bcrypt.checkpw('1'.encode(), s.encode()))