import base64, os, getpass, pyperclip
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken


def encrypt(filepath):
    password1 = getpass.getpass("New password: ")
    password2 = getpass.getpass("Repeat new password: ")

    if password1 == password2:
        salt = os.urandom(16)
        save_salt(salt, filepath)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend()
            )
        plaintext = open(filepath, "r").read().encode()

        key = base64.urlsafe_b64encode(kdf.derive(password1))
        f = Fernet(key)
        token = f.encrypt(plaintext)
        open(filepath.split(".")[0] + "_encrypted", "wb").write(token)
    else:
        print "Passwords don't match"

def decrypt(filepath):
    file = open(filepath, "r").read()
    password = getpass.getpass("Password: ")
    
    salt = get_salt(filepath)


    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=10000,
    backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))

    try:
        f = Fernet(key)
        return f.decrypt(file)

    except InvalidToken:
        print("Found 0 files encrypted with that password.")
        return ""
    
def save_salt(salt, file):
    filename = "." + file.split(".")[0] + "_salt"
    open(filename, "wb").write(salt)
    print("saved salt at " + filename)

def get_salt(filename):
    salt_filename = "." + filename.split("_")[0] + "_salt"
    return open(salt_filename, "rb").read()

def handle_ouput(plaintext, str_command):
    if plaintext != "":

        str_command = str(str_command).lower()

        if str_command == "copy":
            pyperclip.copy(plaintext)
        elif str_command == "print":
            print plaintext
        elif str_command == "save":
            file_name = input("Input file name: ")
            open(file_name, "w").write(plaintext)
            print "Written to " + file_name + " successfuly."
    else:
        return