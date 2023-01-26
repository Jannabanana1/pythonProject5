import hashlib
import random
import string
import math

def hash_preimage(target_string):
    letters = string.ascii_lowercase
    dictionary = {'0': "0000", '1': "0001", '2': "0010", '3': "0011", '4': "0100", '5': "0101", '6': "0110",
                  '7': "0111", '8': "1000", '9': "1001", 'a': "1010", 'b': "1011", 'c': "1100", 'd': "1101",
                  'e': "1110", 'f': "1111"}

    #get length of target string
    length = len(target_string)
    hex_length = math.ceil(length/4)
    bool = False

    while (bool is not True):
        #do i keep randomly generating till it equals the input
        x = "".join(random.choice(letters) for i in range(20))

        #get hash of x of hex_length
        x_hex = hashlib.sha256(x.encode('utf-8')).hexdigest()

        x_hash_last = x_hex[len(x_hex)-hex_length:]

        binary_equivalent = ""
        #convert hash to binary using dictionary
        #for character in x_hash_last:
            #binary_equivalent += dictionary.get(character)
        binary_equivalent = bin(int(x_hex, 16))


        #check if last bits of binary == target_string

        last_bits = binary_equivalent[len(binary_equivalent)-length:]
        if (last_bits == target_string):
            bool = True

        if (bool is True):
            print(target_string)
            print(last_bits)
            print(type(last_bits))
            return x
        else:
            continue

def run():
    print(hash_preimage("1111"))

if __name__ == '__main__':
    run()