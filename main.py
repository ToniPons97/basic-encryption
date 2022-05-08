#!/usr/local/bin/python3
import argparse
from encryption import encrypt, decrypt, handle_ouput

def receiveConfig():
    parser = argparse.ArgumentParser(description="Encryption tool")
    parser.add_argument("-e", "--encrypt", help="Encrypt file.")
    parser.add_argument("-d", "--decrypt", help="Decrypt file.")
    parser.add_argument("-o", "--output", help="Choose output type: (print | copy | save)")
    
    return parser.parse_args()

def main():
    config = receiveConfig()
    if config.encrypt:
        encrypt(config.encrypt)
    elif config.decrypt:
        handle_ouput(decrypt(config.decrypt), config.output)

if __name__ == "__main__":
    main()