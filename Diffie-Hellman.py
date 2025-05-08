import random
import hashlib

class DiffieHellman:
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.private_key = random.randint(2, self.p - 2)
        self.public_key = pow(self.g, self.private_key, self.p)
    
    def generate_shared_secret(self, other_public_key):
        shared_secret = pow(other_public_key, self.private_key, self.p)
        return shared_secret

p = int(input("Enter a prime number (p): "))
g = int(input("Enter a primitive root/generator (g): "))

print("\nAlice is generating her keys...")
alice = DiffieHellman(p, g)
print(f"Alice's private key: {alice.private_key}")
print(f"Alice's public key: {alice.public_key}")

print("\nBob is generating his keys...")
bob = DiffieHellman(p, g)
print(f"Bob's private key: {bob.private_key}")
print(f"Bob's public key: {bob.public_key}")

print("\nAlice and Bob exchange public keys...")

alice_shared_secret = alice.generate_shared_secret(bob.public_key)
bob_shared_secret = bob.generate_shared_secret(alice.public_key)

print("\nShared secrets:")
print(f"Alice's shared secret: {alice_shared_secret}")
print(f"Bob's shared secret: {bob_shared_secret}")

if alice_shared_secret == bob_shared_secret:
    print("\nKey exchange successful! Both parties have the same shared secret.")
else:
    print("\nKey exchange failed!")