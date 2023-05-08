import os
import sys
from lib import libtzxtools as tzx
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("fileName", help="Open specified file")
args = parser.parse_args()

fileName = args.fileName
fileSize = 0
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

if fileName == None:
    print("No input file specified. Please specify a file")
    sys.exit()

tzx.verifyFiles(fileName, "audio")
assignSamples(fileName)

tzx.clipDetect(group1Sample1, group2Sample1, group3Sample1, 'group1Sample1', 'group2Sample1', 'group3Sample1')
tzx.clipDetect(group1Sample1, group2Sample2, group3Sample1, 'group1Sample1', 'group2Sample2', 'group3Sample1')
tzx.clipDetect(group1Sample1, group2Sample3, group3Sample1, 'group1Sample1', 'group2Sample3', 'group3Sample1')

tzx.clipDetect(group1Sample1, group2Sample1, group3Sample2, 'group1Sample1', 'group2Sample1', 'group3Sample2')
tzx.clipDetect(group1Sample1, group2Sample2, group3Sample2, 'group1Sample1', 'group2Sample2', 'group3Sample2')
tzx.clipDetect(group1Sample1, group2Sample3, group3Sample2, 'group1Sample1', 'group2Sample3', 'group3Sample2')

tzx.clipDetect(group1Sample1, group2Sample1, group3Sample3, 'group1Sample1', 'group2Sample1', 'group3Sample3')
tzx.clipDetect(group1Sample1, group2Sample2, group3Sample3, 'group1Sample1', 'group2Sample2', 'group3Sample3')
tzx.clipDetect(group1Sample1, group2Sample3, group3Sample3, 'group1Sample1', 'group2Sample3', 'group3Sample3')

tzx.clipDetect(group1Sample1, group2Sample1, group3Sample4, 'group1Sample1', 'group2Sample1', 'group3Sample4')
tzx.clipDetect(group1Sample1, group2Sample2, group3Sample4, 'group1Sample1', 'group2Sample2', 'group3Sample4')
tzx.clipDetect(group1Sample1, group2Sample3, group3Sample4, 'group1Sample1', 'group2Sample3', 'group3Sample4')
