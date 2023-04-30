import struct
tzxheader = b'\x5A\x58\x54\x61\x70\x65\x21\x1A\x01\x0D'

drum_names = ["kick", "snare", "hipew", "lopew", "HI BEEP", "CL HIHT", "O HIHT", "lO bEeP"]
drum_names_data = bytearray()
audio_block_data = bytearray()
pause_after_block = 26

audio_block_path = './blocks/toybox_audio.bin'
output_file_name = "kit.tzx"

def format_drum_names(name):
# Trim drum names to 7 characters
# pad them with spaces if needed
# make all names uppercase
    name = name[:7]
    name = name.ljust(7)
    name = name.upper()
    return name

def calculate_length(block):
    return(len(block))

def calculate_checksum(block):
    checksum = 0
    for i in block:
        checksum ^= i
    return checksum

#Format Drum Names
drum_names = [format_drum_names(i) for i in drum_names]

# Create drum names block
drum_names_data.insert(0, 0x00)
drum_names_data.extend('c'.encode('UTF-8'))
for i in drum_names:
    drum_names_data.extend(i.encode('UTF-8'))
drum_names_data.append(calculate_checksum(drum_names_data))
drum_names_header = struct.pack('<Bhh', 0x10, pause_after_block, calculate_length(drum_names_data))

# Create audio block

with open(audio_block_path, 'rb') as file:
    audio_block_data.insert(0, 0xFF)
    audio_block_data.extend(file.read())
    audio_block_data.append(calculate_checksum(audio_block_data))
audio_block_header = struct.pack('<Bhh', 0x10, pause_after_block, calculate_length(audio_block_data))

with open(output_file_name, 'wb') as file:
    file.write(tzxheader)
    file.write(drum_names_header)
    file.write(drum_names_data)
    file.write(audio_block_header)
    file.write(audio_block_data)