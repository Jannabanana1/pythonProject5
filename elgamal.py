import random

from params import p
from params import g

def keygen():
    a = random.randint(1, p)
    sk = a #int in range 1..p
    pk = pow(g, a, mod=p) #g^a mod p
    return pk,sk

def encrypt(pk,m):
    r = random.randint(1,p) #q?
    c1 = pow(g, r, mod=p)
    c2 = pow(pk,r, mod=p)
    #what do i do with m here
    return [c1,c2]

def decrypt(sk,c):
    c2 = c[1]
    c1 = c[0]
    m= (c2/(c1**sk)) % sk
    return m

def main():
    keygen()
    decrypt(0,[1,2])
    #encrypt(0,0)
    print("hello")

if __name__ == "__main__":
    main()