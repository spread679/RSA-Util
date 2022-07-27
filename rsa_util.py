#!/usr/bin/env python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from termcolor import colored

def logo():
    print("""
__________  _________   _____               ____ ___   __  .__.__   
\______   \/   _____/  /  _  \             |    |   \_/  |_|__|  |  
 |       _/\_____  \  /  /_\  \    ______  |    |   /\   __\  |  |  
 |    |   \/        \/    |    \  /_____/  |    |  /  |  | |  |  |__
 |____|_  /_______  /\____|__  /           |______/   |__| |__|____/
        \/        \/         \/                                     

""")


def print_task_id():
    print(f"{colored('[0]', 'green')} Quit")
    print(f"{colored('[1]', 'green')} Generate RSA keys")
    print(f"{colored('[2]', 'green')} Encrypt text")
    print(f"{colored('[3]', 'green')} Decrypt text")
    print()


def write_key(filename, key):
    f = open(filename, "wb")
    f.write(key)
    f.close()


def generate_rsa():
    filename = input(f"{colored('[?]', 'blue')} Filename (default mykey): ")
    if not filename:
        filename = "mykey"
        print(f"{colored('[+]', 'green')} Set default filename.")

    format_key = input(f"{colored('[?]', 'blue')} Format (pem, der): ").lower()
        
    if format_key != "pem" or format_key != "der":
        format_key = "pem"
        print(f"{colored('[+]', 'green')} Set default format.")

    passphrase = None

    if input(f"{colored('[?]', 'blue')} Do you want to add a passphrase (y/n)? ").lower() == "y":
            passphrase = input(f"{colored('[?]', 'blue')} Passphrase: ")
    else:
        print(f"{colored('[!]', 'yellow')} No passhphrase, maybe less secure.")
    
    filename_priv = f"{filename}.{format_key}"
    filename_pub = f"{filename}_pub.{format_key}"

    print(f"{colored('[+]', 'green')} Private filename {filename_priv}.")
    print(f"{colored('[+]', 'green')} Public filename {filename_pub}.")
    
    key = RSA.generate(2048)

    write_key(filename_priv, key.export_key(format_key.upper(), passphrase=passphrase))
    write_key(filename_pub, key.publickey().export_key(format_key.upper(), passphrase=passphrase))
    
    print(f"{colored('[+]', 'green')} Generated keys.")
    print()


def encrypt():
    key_file = input(f"{colored('[?]', 'blue')} Enter the public key: ")
                
    file = open(key_file, "r")
    key = RSA.import_key(file.read())
    cipher = PKCS1_OAEP.new(key)
    file.close()

    clear_file = input(f"{colored('[?]', 'blue')} Enter the filename to encrypt: ")
    file_clear = open(clear_file, "r")
    clear_text = file_clear.read().encode('ascii')
    file_clear.close()

    encrypted_text = cipher.encrypt(clear_text)

    file_encrypt = open(f"{clear_file}.encrypt", "wb")
    file_encrypt.write(encrypted_text)
    file_encrypt.close()
    print(f"{colored('[+]', 'green')} Encrypt the file")
    print()


def decrypt():
    key_file = input(f"{colored('[?]', 'blue')} Enter the private key: ")
                
    file = open(key_file, "r")
    key = RSA.import_key(file.read())
    cipher = PKCS1_OAEP.new(key)
    file.close()

    encrypt_file = input(f"{colored('[?]', 'blue')} Enter the filename to decrypt: ")
    file_encrypt = open(encrypt_file, "rb")
    encrypt_text = file_encrypt.read()
    file_encrypt.close()

    clear_text = cipher.decrypt(encrypt_text).decode()

    file_clear = open(f"{encrypt_file}.decrypt", "w")
    file_clear.write(clear_text)
    file_clear.close()
    print(f"{colored('[+]', 'green')} Decrypt the file")
    print()



if __name__ == "__main__":
    logo()
    while True:
        try:
            print_task_id()
            id_task = int(input(f"{colored('[?]', 'blue')}: "))

            if id_task == 0:
                break
            elif id_task == 1:
                generate_rsa()
            elif id_task == 2:
                encrypt()
            elif id_task == 3:
                decrypt()
            else:
                print(f"{colored('[-]', 'red')} Unkwon task id.")
        except Exception as ex:
            print(f"{colored('[-]', 'red')} {ex}")


