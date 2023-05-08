import struct
from lib import libtzxtools as tzx
from argparse import ArgumentParser

program_name = "SpecDrum TZX Builder"

tzxheader = b'\x5A\x58\x54\x61\x70\x65\x21\x1A\x01\x0D'

drum_names = []
drum_names_data = bytearray()
audio_block_data = bytearray()

pause_after_block = 1000 #milliseconds pause between blocks

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

def assignSamples(audio_block_path):
    global group1Sample1 
    global group2Sample1 
    global group2Sample2 
    global group2Sample3 
    global group3Sample1 
    global group3Sample2 
    global group3Sample3 
    global group3Sample4 

    with open(audio_block_path, "rb") as block_file:
        group2Sample1 = bytearray(block_file.read(3072))
        group2Sample2 = bytearray(block_file.read(3072))
        group2Sample3 = bytearray(block_file.read(3072))
        group3Sample1 = bytearray(block_file.read(2048))
        group3Sample2 = bytearray(block_file.read(2048))
        group3Sample3 = bytearray(block_file.read(3072))
        group3Sample4 = bytearray(block_file.read(3072))
        group1Sample1 = bytearray(block_file.read(2048))

tzx.printWelcome(program_name)
tzx.verifyFiles(name_file_path)
tzx.verifyFiles(audio_block_path, "audio")
# Creating names block
print("Creating names block")
# Read first 8 lines of drum names file

#Read first 8 lines of drum names file
with open(name_file_path, 'r') as file:
    drum_names = [next(file) for x in range(8)]

#Format Drum Names
drum_names = [tzx.format_drum_names(drum, idx) for idx, drum in enumerate(drum_names)]
drum_names_data.insert(0, 0x00)
drum_names_data.extend('c'.encode('UTF-8'))
for i in drum_names:
    drum_names_data.extend(i.encode('UTF-8'))
drum_names_data.append(tzx.calculate_checksum(drum_names_data))
drum_names_header = struct.pack('<Bhh', 0x10, pause_after_block, tzx.calculate_length(drum_names_data))
assignSamples(audio_block_path)
print("pause")
tzx.clipDetect(group1Sample1, group2Sample1, group3Sample1, drum_names[0].strip(), drum_names[1].strip(), drum_names[4].strip())
tzx.clipDetect(group1Sample1, group2Sample2, group3Sample1, drum_names[0].strip(), drum_names[2].strip(), drum_names[4].strip())
tzx.clipDetect(group1Sample1, group2Sample3, group3Sample1, drum_names[0].strip(), drum_names[3].strip(), drum_names[4].strip())

tzx.clipDetect(group1Sample1, group2Sample1, group3Sample2, drum_names[0].strip(), drum_names[1].strip(), drum_names[5].strip())
tzx.clipDetect(group1Sample1, group2Sample2, group3Sample2, drum_names[0].strip(), drum_names[2].strip(), drum_names[5].strip())
tzx.clipDetect(group1Sample1, group2Sample3, group3Sample2, drum_names[0].strip(), drum_names[3].strip(), drum_names[5].strip())

tzx.clipDetect(group1Sample1, group2Sample1, group3Sample3, drum_names[0].strip(), drum_names[1].strip(), drum_names[6].strip())
tzx.clipDetect(group1Sample1, group2Sample2, group3Sample3, drum_names[0].strip(), drum_names[2].strip(), drum_names[6].strip())
tzx.clipDetect(group1Sample1, group2Sample3, group3Sample3, drum_names[0].strip(), drum_names[3].strip(), drum_names[6].strip())

tzx.clipDetect(group1Sample1, group2Sample1, group3Sample4, drum_names[0].strip(), drum_names[1].strip(), drum_names[7].strip())
tzx.clipDetect(group1Sample1, group2Sample2, group3Sample4, drum_names[0].strip(), drum_names[2].strip(), drum_names[7].strip())
tzx.clipDetect(group1Sample1, group2Sample3, group3Sample4, drum_names[0].strip(), drum_names[3].strip(), drum_names[7].strip())

# Create audio block
print("Creating audio block")
audio_block_data.insert(0, 0xFF)
audio_block_data.extend(group2Sample1)
audio_block_data.extend(group2Sample2)
audio_block_data.extend(group2Sample3)
audio_block_data.extend(group3Sample1)
audio_block_data.extend(group3Sample2)
audio_block_data.extend(group3Sample3)
audio_block_data.extend(group3Sample4)
audio_block_data.extend(group1Sample1)
audio_block_data.append(tzx.calculate_checksum(audio_block_data))
audio_block_header = struct.pack('<Bhh', 0x10, pause_after_block, tzx.calculate_length(audio_block_data))

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