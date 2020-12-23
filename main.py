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
    elif command[:2] == "ls" or command[:2] == "dir":
        comlen = len(command)
        if comlen >= 4:
            directory = command[3:]
            ls_dir(directory)
        else:
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
    elif command[:4] == "echo":
        string = command[5:]
        echo(string)
    elif command[:5] == "mkdir":
        directory = command[6:]
        mkdir(directory)
    elif command[:2] == "rm":
        if command[3:7] == "-rf ":
            directory = command[7:]
            rm_dir(directory)
        else:
            file_to_remove = command[3:]
            rm(file_to_remove)
    elif command[:5] == "touch":
        file = command[6:]
        touch(file)
    elif command == "help":
        help()
    elif command == "":
        sh()
    elif command == "date":
        date()
    elif command == "exit":
        exit()
    elif command[0] == "!":
        exec = command[1:]
        local_bin(exec)
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
    sh()


# Directory listing
def ls():
    for x in os.listdir('.'):
        print(x)
    sh()


# Directory listing from path
def ls_dir(dir):
    if dir == "~":
        from pathlib import Path
        home = str(Path.home())
        for x in os.listdir(home):
            print(x)
    else:
        for x in os.listdir(dir):
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


# Echo
def echo(str):
    print(str)
    sh()


# Make directory
def mkdir(dir_path):
    os.mkdir(dir_path)
    sh()


# Delete
def rm(file):
    if os.path.exists(file):
        os.remove(file)
        sh()
    else:
        print("1 | File or folder not found : %s" % dir)
        sh()


def rm_dir(dir):
    if os.path.exists(dir):
        os.rmdir(dir)
        sh()
    else:
        print("1 | File or folder not found : %s" % dir)
        sh()


# Create file
def touch(file):
    from pathlib import Path
    if os.path.exists(file):
        overwrite = input('Overwrite existing file %s? (y/N) ' % file)
        if overwrite == "Y" or overwrite == "y":
            Path(file).touch()
        else:
            print('Aborted.')
    Path(file).touch()
    sh()


# Date/Time
def date():
    now = datetime.now()
    print(now)
    sh()


# Local binary execution
def local_bin(binary):
    os.system(binary)
    sh()


# Help
def help():
    print("Welcome to PySH, a UNIX-like shell written entirely in Python.\nAvailable commands:\nhelp: prints this "
          "help\nls <dir>: shows a directory listing\necho <str>: prints text\ncd <dir>: changes the current working "
          "directory\n!<binary>: executes a local binary.\ndate: shows date and time.\ntouch <file>: creates "
          "files\nmkdir <dir>: creates a directory\nrm <file,directory>: removes files/directories\npwd: shows the "
          "path of the current working directory\nversion: shows the version of PySH")
    sh()


sh()
