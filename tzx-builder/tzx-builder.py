import struct
import os
import sys
import re
import numpy as np
from colorama import Fore, Style
from argparse import ArgumentParser

tzxheader = b'\x5A\x58\x54\x61\x70\x65\x21\x1A\x01\x0D'

drum_names = []
drum_names_data = bytearray()
audio_block_data = bytearray()
pause_after_block = 26 #milliseconds pause between blocks

# Paths
name_file_path = ''
audio_block_path = ''
output_file_name = 'kit.tzx' # default, overriden by -o argument

# Arguments

parser = ArgumentParser()
parser.add_argument(dest="name_file", help="Path to drum name file")
parser.add_argument(dest="audio_file", help = "Path to audio block file")
parser.add_argument("-o", "--output", dest="output_file", help="Output file name")
args = parser.parse_args()
name_file_path = args.name_file
audio_block_path = args.audio_file
if args.output_file != None:
    output_file_name = args.output_file

totalClips = 0

def printWelcome():
    print("SpecDrum TZX builder")
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
    if re.search('[^0-9a-zA-Z]+',name):
        print("{}Special characters were found on line {} of name file ({}) and will be removed{}".format(Fore.YELLOW, idx, name, Style.RESET_ALL))
        name = re.sub('[^0-9a-zA-Z]+', '', name)
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

def assignSamples():
    byteOffset = 0

    #Samples
    global group1Sample1 #2048 bytes
    global group2Sample1 #3072 bytes
    global group2Sample2 #3072 bytes
    global group2Sample3 #3072 bytes
    global group3Sample1 #2048 bytes
    global group3Sample2 #2048 bytes
    global group3Sample3 #3072 bytes
    global group3Sample4 #3072 bytes
    global padding


    padding = np.int8([0] * 1024)
    group2Sample1 = np.fromfile(audio_block_path, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group2Sample2 = np.fromfile(audio_block_path, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group2Sample3 = np.fromfile(audio_block_path, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group3Sample1 = np.fromfile(audio_block_path, dtype='int8', count=2048, offset = byteOffset)
    group3Sample1 = np.append(group3Sample1, padding)
    byteOffset += 2048
    group3Sample2 = np.fromfile(audio_block_path, dtype='int8', count=2048, offset = byteOffset)
    group3Sample2 = np.append(group3Sample2, padding)
    byteOffset += 2048
    group3Sample3 = np.fromfile(audio_block_path, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group3Sample4 = np.fromfile(audio_block_path, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group1Sample1 = np.fromfile(audio_block_path, dtype='int8', count=2048, offset = byteOffset)
    group1Sample1 = np.append(group1Sample1, padding)
    byteOffset += 2048

def clipDetect(list1, list2, list3, name1, name2, name3):
    global totalClips
    clipCount = 0
    #convert the lists to use 16 bit ints so that we can see if they exceed the values of 8 bit ints
    list1 = list1.astype('int16')
    list2 = list2.astype('int16')
    list3 = list3.astype('int16')
    #sum the first 2048 bytes of each sample and report any instances of clipping
    for x in range(3072):
        total = list1[x]+list2[x]+list3[x]
        if total >= 128 or total <= -129:
            print("{}Clip @ sample {} when summing {}, {} and {} ({}){}".format(Fore.RED, x, name1, name2, name3, total, Style.RESET_ALL))
            totalClips += 1
    if clipCount == 0:
        print("{}No clips found when summing {}, {} and {}{}".format(Fore.GREEN, name1, name2, name3, Style.RESET_ALL))
    totalClips += clipCount

printWelcome()
verifyFiles(name_file_path)
verifyFiles(audio_block_path, "audio")
# Creating names block
print("Creating names block")
# Read first 8 lines of drum names file

with open(name_file_path, 'r') as file:
    drum_names = [next(file) for x in range(8)]

#Format Drum Names
drum_names = [format_drum_names(drum, idx) for idx, drum in enumerate(drum_names)]
drum_names_data.insert(0, 0x00)
drum_names_data.extend('c'.encode('UTF-8'))
for i in drum_names:
    drum_names_data.extend(i.encode('UTF-8'))
drum_names_data.append(calculate_checksum(drum_names_data))
drum_names_header = struct.pack('<Bhh', 0x10, pause_after_block, calculate_length(drum_names_data))

assignSamples()

clipDetect(group1Sample1, group2Sample1, group3Sample1, drum_names[0].strip(), drum_names[1].strip(), drum_names[4].strip())
clipDetect(group1Sample1, group2Sample2, group3Sample1, drum_names[0].strip(), drum_names[2].strip(), drum_names[4].strip())
clipDetect(group1Sample1, group2Sample3, group3Sample1, drum_names[0].strip(), drum_names[3].strip(), drum_names[4].strip())

clipDetect(group1Sample1, group2Sample1, group3Sample2, drum_names[0].strip(), drum_names[1].strip(), drum_names[5].strip())
clipDetect(group1Sample1, group2Sample2, group3Sample2, drum_names[0].strip(), drum_names[2].strip(), drum_names[5].strip())
clipDetect(group1Sample1, group2Sample3, group3Sample2, drum_names[0].strip(), drum_names[3].strip(), drum_names[5].strip())

clipDetect(group1Sample1, group2Sample1, group3Sample3, drum_names[0].strip(), drum_names[1].strip(), drum_names[6].strip())
clipDetect(group1Sample1, group2Sample2, group3Sample3, drum_names[0].strip(), drum_names[2].strip(), drum_names[6].strip())
clipDetect(group1Sample1, group2Sample3, group3Sample3, drum_names[0].strip(), drum_names[3].strip(), drum_names[6].strip())

clipDetect(group1Sample1, group2Sample1, group3Sample4, drum_names[0].strip(), drum_names[1].strip(), drum_names[7].strip())
clipDetect(group1Sample1, group2Sample2, group3Sample4, drum_names[0].strip(), drum_names[2].strip(), drum_names[7].strip())
clipDetect(group1Sample1, group2Sample3, group3Sample4, drum_names[0].strip(), drum_names[3].strip(), drum_names[7].strip())

if totalClips > 0:
    print()
    print(Fore.RED + str(totalClips) + Style.RESET_ALL + ' total clips')
else:
    print(Style.RESET_ALL + "No clips found")

# Create audio block
print("Creating audio block")
audio_block_data.insert(0, 0xFF)
with open(audio_block_path, 'rb') as file:  
    audio_block_data.extend(file.read())
audio_block_data.append(calculate_checksum(audio_block_data))
audio_block_header = struct.pack('<Bhh', 0x10, pause_after_block, calculate_length(audio_block_data))

try:
    with open(output_file_name, 'wb') as file:
        print("Writing TZX header")
        file.write(tzxheader)
        print("Writing names block header")
        file.write(drum_names_header)
        print("Writing names block data")
        file.write(drum_names_data)
        print("Writing audio block header")
        file.write(audio_block_header)
        print("Writing audio block data")
        file.write(audio_block_data)
        print("TZX file successfully written to {}".format(output_file_name))
except:
    print("Output file {} could not be written. Check that it is not read only and that you have the neccesary file/folder permissions".format(output_file_name))