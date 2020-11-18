#basic-encryption

This is a simple password manager that I created to help me manage a bunch of trivial passwords.

I tried to make the utility as simple as possible. It has only two options: 
encrypt file and decrypt file. When you encrypt a file the salt is saved as a 
hidden file in the same directory where main.py lives. For the program to
work it should be ran from the same directory where main.py is. This issue 
will be fixed someday without pressure.

If you do ./main.py --help you'll see how straight forward it is.

To encrypt file:
	./main.py -e file.txt
The program will ask you for a password. After that it will generate a hashed
file and its corresponding salt. Don't delete the salt if you wish to
unencrypt it later. Ideally both the hash and the salt should be saved to a 
database (I'm thinking SQLite).

To decrypt file:
	./main.py -d file.txt
It will ask you for the password. After entering the password you'll have the
original message copied to your clipboard, so if you do COMMAND + V (or CTRL + V) you'll see that the message is copied.