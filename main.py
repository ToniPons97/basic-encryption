#!/usr/bin/python
import argparse
from encryption import encrypt, decrypt

def receiveConfig():
    parser = argparse.ArgumentParser(description="Encryption tool")
    parser.add_argument("-e", "--encrypt", help="Encrypt file")
    parser.add_argument("-d", "--decrypt", help="Decrypt file")
    return parser.parse_args()

def main():
    config = receiveConfig()

    if config.encrypt:
        encrypt(config.encrypt)
    if config.decrypt:
        decrypt(config.decrypt)

if __name__ == "__main__":
    main()