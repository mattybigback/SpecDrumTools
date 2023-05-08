import os
import sys
import re
from colorama import Fore, Style

def printWelcome(program_name):
    print(program_name)
    print("mjharrison.co.uk")

def verifyFiles(file, type=None):
    if type != "audio":
        type = "names"
    try:
        fileStats = os.stat(file)
        fileSize = fileStats.st_size
    except FileNotFoundError:
        print("File \"" + file + "\" not found")
        sys.exit()
    if fileSize != 21504 and type == "audio":
        print ('File is not a valid SpecDrum audio data block')
        print (f'File size invalid - {fileStats.st_size} bytes')
        sys.exit()
    if type == "names":
        with open(file, 'r') as input_file:
            file_number_of_lines = len(input_file.readlines())
        if file_number_of_lines < 8:
            print("{}{} file \"{}\" invalid - not enough lines: ({}/8){}".format(Fore.RED,type.title(), file, file_number_of_lines, Style.RESET_ALL))
            sys.exit()
        if fileSize > 100:
            print("{}{} file \"{}\" invalid - too large. {}".format(Fore.RED, type.title(), file, Style.RESET_ALL))
            sys.exit()
    print("{} file \"{}\" exists and is valid".format(type.title(), file))

def format_drum_names(name, idx):
    idx=idx+1
    name = name.strip()
    if re.search('[^0-9a-zA-Z ]+',name):
        print("{}Special characters were found on line {} of name file ({}) and will be removed{}".format(Fore.YELLOW, idx, name, Style.RESET_ALL))
        name = re.sub('[^0-9a-zA-Z ]+', '', name)
    name = name[:7]
    name = name.ljust(7)
    name = name.upper()
    if name == '       ':
        name = "{}      ".format(idx)
        print("{}Drum {} name is blank, replacing name with slot number ({}){}".format(Fore.YELLOW, idx, name.strip(), Style.RESET_ALL))
    return name

def calculate_length(block):
    print("Calculating block length", end='')
    print ("{} {}{}".format(Fore.YELLOW, len(block), Style.RESET_ALL))
    return(len(block))

def calculate_checksum(block):
    checksum = 0
    print("Calculating block checksum... ", end="")
    for i in block:
        checksum ^= i
    print(Fore.YELLOW + hex(checksum) + Style.RESET_ALL)
    return checksum

def to_signed_int8(n):
    n = n & 0xff
    return n | (-(n & 0x80))

def clipDetect(list1, list2, list3, name1, name2, name3):
    lists = []
    lists.append(list1.copy())
    lists.append(list2.copy())
    lists.append(list3.copy())
    padding = bytearray(1024)
    clipCount = 0
    for i in lists:
        if len(i) < 3072:
            i.extend(padding)

    #convert the lists to use 16 bit ints so that we can see if they exceed the values of 8 bit ints
    for x in range(3072):
        total = to_signed_int8(lists[0][x])+to_signed_int8(lists[1][x])+to_signed_int8(lists[2][x])
        if total >= 128 or total <= -129:
            print("{}Clip @ sample {} when summing {}, {} and {} ({}){}".format(Fore.RED, x, name1, name2, name3, total, Style.RESET_ALL))
            clipCount += 1
    if clipCount == 0:
        print("{}No clips found when summing {}, {} and {}{}".format(Fore.GREEN, name1, name2, name3, Style.RESET_ALL))
    return clipCount