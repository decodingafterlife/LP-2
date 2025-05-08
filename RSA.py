import math
import random

class RSA:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p*q
        self.phi_n = self.get_totient(self.p, self.q)
        self.e = self.get_e(self.phi_n)
        self.public_key = self.get_public_key(self.e, self.n)
        self.d = self.get_d(self.e, self.phi_n)
        self.private_key = self.get_private_key(self.d, self.n)

    def extended_euclid(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_euclid(b%a, a)
            return gcd, y - (b//a) * x, x

    def get_totient(self, p, q):
        return (p-1)*(q-1)

    def get_e(self, phi_n):
        e = 0
        while e == 0:
            for i in range(2, phi_n):
                if math.gcd(phi_n, i) == 1 and random.random() > 0.7:
                    e = i
                    break
        return e
            
    
    def get_d(self, e, phi_n):
        gcd, x, y = self.extended_euclid(e, phi_n)
        return x % phi_n

    # def get_d(self, e, phi_n):
    #     gcd, x, y = self.extended_euclid(e, phi_n)
    #     # Make sure d is positive
    #     return (x % phi_n + phi_n) % phi_n
    
    def get_public_key(self, e, n):
        return [e, n]

    def get_private_key(self, d, n):
        return [d, n]

    def encryption(self, M,  public_key):
        return pow(M, public_key[0], public_key[1])

    def decryption(self, M,  private_key):
        return pow(M, private_key[0], private_key[1])


p = int(input('Enter prime number 1: '))
q = int(input('Enter prime number 2: '))
obj = RSA(p,q)

print('n: ', obj.n)
print('phi_n: ', obj.phi_n)
print('e: ', obj.e)
print('d: ', obj.d)
print('public key: ', obj.public_key)
print('private key: ', obj.private_key)

M = int(input('Enter decimal number: '))
C = obj.encryption(M, obj.public_key)
print('ciphertext : ', C)
M_2 = obj.decryption(C, obj.private_key)
print('decrypted message: ', M_2)