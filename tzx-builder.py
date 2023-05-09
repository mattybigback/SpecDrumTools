""" Builds SpecDrum TZX files from a list of drum names and an audio block"""
import struct
from argparse import ArgumentParser
from lib import libtzxtools as tzx


program_name = "SpecDrum TZX Builder"
tzx_header_block = b'\x5A\x58\x54\x61\x70\x65\x21\x1A\x01\x0D'
drum_names = []
drum_names_data = bytearray()
audio_block_data = bytearray()
pause_after_block = 1000 #milliseconds pause between blocks

# Audio Sample Storage
group1Sample1 = bytearray()
group2Sample1 = bytearray()
group2Sample2 = bytearray()
group2Sample3 = bytearray()
group3Sample1 = bytearray()
group3Sample2 = bytearray()
group3Sample3 = bytearray()
group3Sample4 = bytearray()
group_samples = [[group2Sample1, 3072], [group2Sample2, 3072],[group2Sample3, 3072], [group3Sample1, 2048], [group3Sample2, 2048], [group3Sample3,3072], [group3Sample4, 3072], [group1Sample1, 2048]]

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
if args.output_file is not None:
    output_file_name = args.output_file

tzx.print_welcome(program_name)
tzx.verify_file(name_file_path)
tzx.verify_file(audio_block_path, "audio")
# Creating names block
print("Creating names block")
# Read first 8 lines of drum names file

#Read first 8 lines of drum names file
with open(name_file_path, 'r', encoding='UTF-8') as file:
    drum_names = [next(file) for x in range(8)]

#Format Drum Names
drum_names = [tzx.format_drum_names(drum, idx) for idx, drum in enumerate(drum_names)]
drum_names_data.insert(0, 0x00)
drum_names_data.extend('c'.encode('UTF-8'))
for i in drum_names:
    drum_names_data.extend(i.encode('UTF-8'))
drum_names_data.append(tzx.calculate_checksum(drum_names_data))
drum_names_header = struct.pack('<Bhh', 0x10, pause_after_block, tzx.calculate_length(drum_names_data))
group_samples = tzx.assign_samples(audio_block_path, group_samples)

for sample1 in group_samples[0:3]:
    for sample2 in group_samples[4:7]:
        for i, drum_name in enumerate(drum_names[1:4]):
            clip_count = 0
            clip_count += tzx.detect_clips(group_samples[7][0], sample1[0], sample2[0], drum_names[0].strip(), drum_name.strip(), drum_names[i+4].strip())
print("{} clips found".format(clip_count))

# Create audio block
print("Creating audio block")
audio_block_data.insert(0, 0xFF)
for idx_sample, sample in enumerate(group_samples):
    audio_block_data.extend(group_samples[idx_sample][0])
audio_block_data.append(tzx.calculate_checksum(audio_block_data))
audio_block_header = struct.pack('<Bhh', 0x10, pause_after_block, tzx.calculate_length(audio_block_data))

try:
    with open(output_file_name, 'wb') as file:
        print("Writing TZX header")
        file.write(tzx_header_block)
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