import random

from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256


def sign(m):
    # generate public key
    # Your code here

    # generate signature
    # Your code here
    public_key = dG
    k = random.randint(1,p)
    (x1, y2) = kG
    r = x1 % n
    z = Hash(m)
    s = k**-1(z+rd) % n


    assert isinstance(public_key, point.Point)
    assert isinstance(r, int)
    assert isinstance(s, int)
    return (public_key, [r, s])


