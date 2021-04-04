import sys
import os
from argparse import ArgumentParser

XORcypher = bytearray("  1986. A Pateman & P Hennig.  ", 'utf-8') #byte array containing string to be XORed

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="inputFileName", help="Open specified file")
parser.add_argument("-o", "--output", dest="outputFileName", help="Specify output file name")
args = parser.parse_args()

def printWelcome():
    print("AmDrum File Converter")
    print("m-harrison.org")

def verifyFiles():
    if args.inputFileName == None:
        print('No input file specified. Please specify a file path using -i.')
        sys.exit()

    try:
        fileStats = os.stat(args.inputFileName)
        fileSize = fileStats.st_size
    except FileNotFoundError:
        print("Input file not found")
        sys.exit()

    if fileSize != 21504:
        print ('File is not a valid SpecDrum/AmDrum audio data block')
        print (f'File size invalid - {fileStats.st_size} bytes')
        sys.exit()

if args.outputFileName == None:
    outputFileName = "output.bin"
else:
    outputFileName = str(args.outputFileName)

verifyFiles()
printWelcome()

inputFile = bytearray(open(str(args.inputFileName), 'rb').read()) #Load file to be XORed as byte array
size = len(inputFile) #Get size of input file in bytes
xorBuffer = bytearray(size) #Create empty array for output

for i in range(size):
    xorBuffer[i] = inputFile[i] ^ XORcypher[i%32]
open(outputFileName,'wb').write(xorBuffer) #Write output to disk

print(outputFileName + " created successfully")

