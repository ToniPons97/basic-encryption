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

        key = base64.urlsafe_b64encode(kdf.derive(bytes(password1, 'utf-8')))
        f = Fernet(key)
        token = f.encrypt(plaintext)
        open(filepath.split(".")[0] + "_encrypted", "wb").write(token)


        r_u_done = 0
        while r_u_done < 3:
            option = input("File encrypted successfully.\nDo you wish to delete " + filepath + "? ").lower()
            if (option == "yes" or option == "y"):
                print("Deleting " + filepath)
                os.remove(filepath)
                print("Done!")
                r_u_done = 3
            else:
                print("Ok bye!")
                r_u_done = 3
            r_u_done += 1
    else:
        print("Passwords don't match")

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
    key = base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))

    try:
        f = Fernet(key)
        return f.decrypt(bytes(file, 'utf-8'))

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

        if str_command == "copy":
            pyperclip.copy(decode_data(plaintext))
        elif str_command == "print":
            print(decode_data(plaintext))
        elif str_command == "save":
            file_name = input("Input file name: ")
            open(file_name, "wb").write(plaintext)
            print("Written to " + file_name + " successfuly.")
    else:
        return

def decode_data(plaintext):
    decoded_data = ''.join(map(chr, plaintext))
    return repr(decoded_data)