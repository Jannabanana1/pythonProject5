
def encrypt(key,plaintext):
    ciphertext=""
    for letter in plaintext:
        i = ord(letter)
        if (i+key) > ord('Z'):
            i -= 26
        encrypted = i + key
        encrypted = chr(encrypted)
        ciphertext += encrypted
    print(ciphertext)
    return ciphertext

def decrypt(key,ciphertext):
    plaintext=""
    for letter in ciphertext:
        i = ord(letter)
        if (i-key) < ord('A'):
            i += 26
        decrypted = i - key
        decrypted = chr(decrypted)
        plaintext += decrypted
    return plaintext


def main():
    encrypt(11,"NAKAMOTO")
    print("hell0o")


if __name__ == "__main__":
    main()

