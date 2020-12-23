# Python Shell (PySH) by Nicolas Mailloux. Designed entirely in Python, with UNIX philosophy in mind.
# The programs included in this project are free software.
# PySH comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.

from datetime import datetime
from datetime import date
import getpass
import socket
import pathlib
import os

# Defining some variables
version = 0.1

# Init process
# Getting user's name & computer hostname
user = getpass.getuser()
hostname = socket.gethostname()
# Greeting the user
print("Welcome to PySH v%s" % version)
now = datetime.now()
day = date.today()
time = now.strftime("%H:%M:%S")
date = day.strftime("%B %d, %Y")
print("It is {0} | {1}\n".format(date, time))


# Shell prompt
def sh():
    # Get current directory
    current_dir = pathlib.Path().absolute()
    command = input("{0}@{1}:{2} $ ".format(user, hostname, current_dir))
    if command == "version":
        get_version()
    elif command == "pwd":
        pwd()
    elif command == "ls":
        ls()
    elif command[:2] == "cd":
        comlen = len(command)
        if comlen >= 4:
            directory = command[3:]
            cd(directory)
        else:
            from pathlib import Path
            home = str(Path.home())
            os.chdir(home)
            sh()
    elif command == "exit":
        exit()
    else:
        print("127 | Command not found : %s" % command)
        sh()


# Version
def get_version():
    print(version)
    # Recall shell prompt
    sh()


# Current directory path
def pwd():
    current_dir = pathlib.Path().absolute()
    print(current_dir)
    # Recall shell prompt
    sh()


# Directory listing
def ls():
    for x in os.listdir('.'):
        print(x)
    sh()


# Change directory
def cd(dir):
    if dir == "~":
        from pathlib import Path
        home = str(Path.home())
        os.chdir(home)
    else:
        os.chdir(dir)
    sh()


sh()
