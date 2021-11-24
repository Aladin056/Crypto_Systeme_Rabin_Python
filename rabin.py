from Crypto.Util.number import isPrime,getPrime, inverse
import math 
import random
from math import gcd
import hashlib

#tableau des entiers premiers 
def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True

        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)
            
    return prime_list

#creer la list des entier premier 
prime_list = primesInRange(100,500)


def encryption(msg, n):
    # c = m^2 mod n
    #convertir le message en entier
    msg_int = int.from_bytes(msg.encode('utf-8'),'big')
    return msg_int ** 2 % n

def racine_carée_3_mod_4(a, p):
    r = pow(a, (p + 1) // 4, p)
    return r


def racine_carée_5_mod_8(a, p):
    d = pow(a, (p - 1) // 4, p)
    r =0
    if d == 1:
        r = pow(a, (p + 3) // 8, p)
    elif d == p - 1:
        r = 2 * a * pow(4 * a, (p - 5) // 8, p) % p

    return r

#Pour choisir le bon message
def choisir(lst,b):

    for i in lst:  
        if i == b:
            return int(i)
    return int(i)
    
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, y, x = egcd(b % a, a)
        return gcd, x - (b // a) * y, y

def decryption(a, p, q,c):
    n = int(p * q)
    r, s = 0, 0
    if p % 4 == 3:
        r = racine_carée_3_mod_4(a, p)
    elif p % 8 == 5:
        r = racine_carée_5_mod_8(a, p)
    if q % 4 == 3:
        s = racine_carée_3_mod_4(a, q)
    elif q % 8 == 5:
        s = racine_carée_5_mod_8(a, q)

    gcd, c, d = egcd(p, q)
    x = int((r * d * q + s * c * p) % n)
    y = int((r * d * q - s * c * p) % n)
    lst = [x, n - x, y, n - y]

    int_entrer = choisir(lst,c) #c c'est le message non crypté en entier 
    int_msg=int_entrer.to_bytes((int_entrer.bit_length() + 7) // 8, 'big').decode('utf-8')
    

    return int_msg


#generer les Clé 
p=random.choice(prime_list)
q=random.choice(prime_list)
n=p*q #Clé publique 


msg = input('message  = ')
msg_int= int.from_bytes(msg.encode('utf-8'),'big') #pour garder la valeur initale de message en entier

msg_crypt_int = encryption(msg, n)
print("\n\n")

print('Message crypté en entier  = '+ str(msg_crypt_int))
print("\n\n")

msg_crypt=int(msg_crypt_int).to_bytes((int(msg_crypt_int).bit_length() + 7) // 8, 'big').decode('utf-8')
print('Message crypté en caratere  = '+msg_crypt)


crypt_msg = decryption(msg_crypt_int, p, q,msg_int)
print('Le message = '+crypt_msg)
