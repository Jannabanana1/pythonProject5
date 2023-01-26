import hashlib
import os
import random
import string
import math


def hash_collision(k):
    if not isinstance(k, int):
        print("hash_collision expects an integer")
        return (b'\x00', b'\x00')
    if k < 0:
        print("Specify a positive number of bits")
        return (b'\x00', b'\x00')

    # Collision finding code goes here
    x = b'\x00'
    y = b'\x00'

    num_hexadecimals = math.ceil(k / 4)  # rounds up number of hexadecimals

    # dictionary for
    dictionary = {'0': "0000", '1': "0001", '2': "0010", '3': "0011", '4': "0100", '5': "0101", '6': "0110",
                  '7': "0111", '8': "1000", '9': "1001", 'a': "1010", 'b': "1011", 'c': "1100", 'd': "1101",
                  'e': "1110", 'f': "1111"}

    # below is my codee
    letters = string.ascii_lowercase
    # generates random alphabet up to 20 characters
    x = ''.join(random.choice(letters) for i in range(20))
    x_hex = hashlib.sha256(x.encode('utf-8')).hexdigest()  # returns hexadecimal
    last_hex_characters_x = x_hex[len(x_hex) - num_hexadecimals:]

    binary_equivalent_x = ""
    for character in last_hex_characters_x:
        binary_equivalent_x += dictionary.get(character)
    byte_str_x = x_hex.encode('utf-8')

    bool = False
    while (bool is not True):
        # keep generating y till it equals x
        y = ''.join(random.choice(letters) for i in range(20))

        # generates a hash
        y_hex = hashlib.sha256(y.encode('utf-8')).hexdigest()

        byte_str_y = y_hex.encode('utf-8')

        # gets last hex characters rounded from k
        last_hex_characters_y = y_hex[len(y_hex) - num_hexadecimals:]

        # convert hex to binary
        binary_equivalent_y = ""

        for item in last_hex_characters_y:
            binary_equivalent_y += dictionary.get(item)

        # stores last k digits into a variable
        lastk_binary_digits_x = binary_equivalent_x[len(binary_equivalent_x) - k:]
        lastk_binary_digits_y = binary_equivalent_y[len(binary_equivalent_y) - k:]

        # checks if last k digits of x and y are equal
        if (lastk_binary_digits_x == lastk_binary_digits_y):
            bool = True

        if (bool is True):
            x = x.encode('utf-8')
            y = y.encode('utf-8')

            return (x, y)
        else:
            continue


def run():
    print(hash_collision(2))


if __name__ == '__main__':
    run()
