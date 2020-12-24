# Python Shell (PySH) by Nicolas Mailloux. Designed entirely in Python, with UNIX philosophy in mind. Includes
# several base utility programs. The programs included in this project are free software.
# PySH comes with ABSOLUTELY NO WARRANTY, to the extent permitted by applicable law.

from datetime import datetime
from datetime import date
from shutil import copyfile
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
    command = input("\033[96;1m{0}\033[0m@{1}:\033[1m{2}\033[0m $ ".format(user, hostname, current_dir))
    if command == "version":
        get_version()
    elif command == "pwd":
        pwd()
    elif command[:2] == "ls" or command[:2] == "dir":
        comlen = len(command)
        if comlen >= 4:
            if command[:4] == "ls -":
                if command[4] == "a":
                    if comlen == 5:
                        ls("TRUE")
                    else:
                        directory = command[6:]
                        ls_dir(directory, "TRUE")
            else:
                directory = command[3:]
                ls_dir(directory, "FALSE")

        else:
            ls("FALSE")
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
    elif command[:2] == "cp":
        comlen = len(command)
        if command == "cp":
            print("\033[91;1m1\033[0m | Missing source and/or destination")
            sh()
        if comlen >= 4:
            s = command.split()
            slen = len(s)
            if slen == 2:
                print("\033[91;1m1\033[0m | Missing source and/or destination")
                sh()
            elif slen >= 4:
                print("\033[91;1m1\033[0m | Too many arguments")
                sh()
            elif slen == 3:
                source_file = s[1]
                copied_file = s[2]
                cp(source_file, copied_file)
    elif command[:3] == "cat":
        comlen = len(command)
        s = command.split()
        slen = len(s)
        if comlen == 3:
            print("\033[91;1m1\033[0m | Missing file")
            sh()
        elif slen >= 3:
            print("\033[91;1m1\033[0m | Too many arguments")
            sh()
        else:
            printfile = s[1]
            if os.path.exists(printfile):
                file = open(printfile)
                line = file.read()
                file.close()
                print(line)
            else:
                print("\033[91;1m1\033[0m | No such file or directory")
            # print("cat is not usable at the moment due to a bug. Please check the GitHub page for updates on the project.")
            sh()
            # cat(printfile)
    elif command == "exit":
        exit()
    # To be changed to analysing PATH and executing the correct binary if not present in the shell. If user still
    # doesn't want to run the included bundle, then specifying "!" in front of the command will run the local binary.
    elif command[0] == "!":
        exec = command[1:]
        local_bin(exec)
    else:
        print("\033[91;1m127\033[0m | Command not found : %s" % command)
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
def ls(list_all):
    current_dir = pathlib.Path().absolute()
    if os.path.exists(current_dir):
        if list_all == "TRUE":
            for x in os.listdir():
                print(x)
        else:
            for x in os.listdir('.'):
                if x[0] == ".":
                    pass
                else:
                    print(x)
    else:
        print("\033[91;1m1\033[0m | No such file or directory")
    sh()


# Directory listing from path
def ls_dir(dir, list_all):
    if dir == "~":
        from pathlib import Path
        home = str(Path.home())
        for x in os.listdir(home):
            if list_all == "TRUE":
                print(x)
            else:
                if x[0] == ".":
                    pass
                else:
                    print(x)
    else:
        if os.path.exists(dir):
            for x in os.listdir(dir):
                if list_all == "TRUE":
                    print(x)
                else:
                    if x[0] == ".":
                        pass
                    else:
                        print(x)
        else:
            print("\033[91;1m1\033[0m | No such file or directory")
    sh()


# Change directory
def cd(dir):
    if dir == "~":
        from pathlib import Path
        home = str(Path.home())
        os.chdir(home)
    else:
        if os.path.exists(dir):
            os.chdir(dir)
        else:
            print("\033[91;1m1\033[0m | No such file or directory")
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
        print("\033[91;1m1\033[0m | File or folder not found : %s" % dir)
        sh()


def rm_dir(dir):
    if os.path.exists(dir):
        os.rmdir(dir)
        sh()
    else:
        print("\033[91;1m1\033[0m | File or folder not found : %s" % dir)
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


# File copy
def cp(source, destination):
    copyfile(source, destination)
    sh()


# Print a file's contents //// NOT WORKING
"""
def cat(print):
    file = open(print)
    line = file.read()
    file.close()
    print(line)
    sh()
"""


# Help
def help():
    print("\033[94;1mWelcome to PySH, an UNIX-like, cross-platform shell written entirely in Python.\033["
          "0m\nAvailable commands:\nhelp: prints this "
          "help\nls <dir>: shows a directory listing\necho <str>: prints text\ncd <dir>: changes the current working "
          "directory\n!<binary>: executes a local binary.\ndate: shows date and time.\ntouch <file>: creates "
          "files\ncat: prints a file's content\nmkdir <dir>: creates a directory\nrm <file,directory>: removes "
          "files/directories\ncp: copies "
          "files\npwd: shows the path of the current working directory\nversion: shows the version of PySH")
    sh()


sh()
