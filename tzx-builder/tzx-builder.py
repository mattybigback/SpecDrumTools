import struct
import os
import sys
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
            print("{} file \"{}\" invalid - not enough lines: ({})".format(type.title(), file, file_number_of_lines))
            sys.exit()
    print("{} file \"{}\" exists and is valid".format(type.title(), file))

def format_drum_names(name):
# Trim drum names to 7 characters
# pad them with spaces if needed
# make all names uppercase
    name = name.strip()
    name = name[:7]
    name = name.ljust(7)
    name = name.upper()
    return name

def calculate_length(block):
    print("Calculating block length")
    return(len(block))

def calculate_checksum(block):
    checksum = 0
    print("Calculating block checksum")
    for i in block:
        checksum ^= i
    return checksum


printWelcome()
verifyFiles(name_file_path)
verifyFiles(audio_block_path, "audio")
# Creating names block
print("Creating names block")
# Read first 8 lines of drum names file

with open(name_file_path, 'r') as file:
    drum_names = [next(file) for x in range(8)]

#Format Drum Names
drum_names = [format_drum_names(i) for i in drum_names]
drum_names_data.insert(0, 0x00)
drum_names_data.extend('c'.encode('UTF-8'))
for i in drum_names:
    drum_names_data.extend(i.encode('UTF-8'))
drum_names_data.append(calculate_checksum(drum_names_data))
drum_names_header = struct.pack('<Bhh', 0x10, pause_after_block, calculate_length(drum_names_data))

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