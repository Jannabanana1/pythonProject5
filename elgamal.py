import random

from params import p
from params import g

def keygen():
    sk = random.randint(1, p)
    pk = pow(g, sk, p) #g^a mod p
    return pk,sk

def encrypt(pk,m):
    r = random.randint(1,p)
    c1 = pow(g, r, p)

    c2 = pow(pk,r,p)
    c2 = c2* m %p
    return [c1,c2]


def mod_inverse(a, m):
    pass


def decrypt(sk,c):
    #c2 = c[1]
    #c1 = c[0]
    m = mod_inverse(pow(c[0],sk,p),p)
    m = m*c[1] %p
    #(c2/(c1**sk)) % sk
    return m
