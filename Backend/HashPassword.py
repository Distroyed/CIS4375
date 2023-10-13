import hashlib

plaintext_password = "1"  #replace this with the password you want to hash

password = plaintext_password.encode('utf-8')
hashed_password = hashlib.sha256(password).hexdigest()

print("Plaintext Password:", plaintext_password)
print("Hashed Password:", hashed_password)

