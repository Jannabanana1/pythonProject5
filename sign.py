
from fastecdsa.curve import secp256k1
from fastecdsa.keys import export_key, gen_keypair

from fastecdsa import curve, ecdsa, keys, point
from hashlib import sha256


def sign(m):
    # generate public key
    # Your code here

    # generate signature
    # Your code here
   #returns a tuple of private key, then public key

    tuple = keys.gen_keypair(secp256k1)

    r,s = ecdsa.sign(m,tuple[0],curve = curve.secp256k1,hashfunc=sha256)
    public_key = tuple[1]

    assert isinstance(public_key, point.Point)
    assert isinstance(r, int)
    assert isinstance(s, int)
    return (public_key, [r, s])


