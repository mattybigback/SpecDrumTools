import os
import numpy as np
import sys
from argparse import ArgumentParser
from colorama import Fore, Style

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="fileName", help="Open specified file")
args = parser.parse_args()

fileName = args.fileName
fileSize = 0
totalClips = 0


print("Specdrum Clip Detector")
print("m-harrison.org")

def verifyFiles():
    try:
        file_stats = os.stat(fileName)
        fileSize = file_stats.st_size
    except FileNotFoundError:
        print("File not found")
        sys.exit()
    if fileSize != 21504:
        print ('File is not a valid SpecDrum audio data block')
        print (f'File size invalid - {file_stats.st_size} bytes')
        sys.exit()
    else:
        print ('File is valid')
        

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

    group2Sample1 = np.fromfile(fileName, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group2Sample2 = np.fromfile(fileName, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group2Sample3 = np.fromfile(fileName, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group3Sample1 = np.fromfile(fileName, dtype='int8', count=2048, offset = byteOffset)
    byteOffset += 2048
    group3Sample2 = np.fromfile(fileName, dtype='int8', count=2048, offset = byteOffset)
    byteOffset += 2048
    group3Sample3 = np.fromfile(fileName, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group3Sample4 = np.fromfile(fileName, dtype='int8', count=3072, offset = byteOffset)
    byteOffset += 3072
    group1Sample1 = np.fromfile(fileName, dtype='int8', count=2048, offset = byteOffset)
    byteOffset += 2048

    
def clipDetect(list1, list2, list3, name1, name2, name3):
    global totalClips
    clipCount = 0
    #convert the lists to use 16 bit ints so that we can see if they exceed the values of 8 bit ints
    list1 = list1.astype('int16')
    list2 = list2.astype('int16')
    list3 = list3.astype('int16')
    #sum the first 2048 bytes of each sample and report any instances of clipping
    for x in range(2048):
        total = list1[x]+list2[x]+list3[x]
        if total >= 128 or total <= -129:
            print(Fore.RED + 'Clipping at index ' + str(x) +' when adding ' + name1 + ', ' + name2 + ' and ' + name3 + ' ('+ str(total) +')')
            totalClips += 1
    if clipCount == 0:
        print(Fore.GREEN + 'No clips found between ' + name1 + ', ' + name2 +' and ' + name3)
    totalClips += clipCount


if fileName == None:
    print('No input file specified. Please specify a file path using -i.')
    sys.exit()

verifyFiles()
assignSamples()

clipDetect(group1Sample1, group2Sample1, group3Sample1, 'group1Sample1', 'group2Sample1', 'group3Sample1')
clipDetect(group1Sample1, group2Sample2, group3Sample1, 'group1Sample1', 'group2Sample2', 'group3Sample1')
clipDetect(group1Sample1, group2Sample3, group3Sample1, 'group1Sample1', 'group2Sample3', 'group3Sample1')

clipDetect(group1Sample1, group2Sample1, group3Sample2, 'group1Sample1', 'group2Sample1', 'group3Sample2')
clipDetect(group1Sample1, group2Sample2, group3Sample2, 'group1Sample1', 'group2Sample2', 'group3Sample2')
clipDetect(group1Sample1, group2Sample3, group3Sample2, 'group1Sample1', 'group2Sample3', 'group3Sample2')

clipDetect(group1Sample1, group2Sample1, group3Sample3, 'group1Sample1', 'group2Sample1', 'group3Sample3')
clipDetect(group1Sample1, group2Sample2, group3Sample3, 'group1Sample1', 'group2Sample2', 'group3Sample3')
clipDetect(group1Sample1, group2Sample3, group3Sample3, 'group1Sample1', 'group2Sample3', 'group3Sample3')

clipDetect(group1Sample1, group2Sample1, group3Sample4, 'group1Sample1', 'group2Sample1', 'group3Sample4')
clipDetect(group1Sample1, group2Sample2, group3Sample4, 'group1Sample1', 'group2Sample2', 'group3Sample4')
clipDetect(group1Sample1, group2Sample3, group3Sample4, 'group1Sample1', 'group2Sample3', 'group3Sample4')

if totalClips > 0:
    print()
    print(Fore.RED + str(totalClips) + Style.RESET_ALL + ' total clips')
else:
    print()
    print(Style.RESET_ALL + "No clips found")
