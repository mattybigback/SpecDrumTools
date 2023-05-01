# SpecDrum Tools
Tools for making custom kits for the Cheetah SpecDrum

## tzx-builder

Creates a TZX file that can be loaded into the SpecDrum software. This release incorporates the clip detector code, so there is no need to download it separately.

### Usage
```
 tzx-builder.exe  name_file audio_file [-o OUTPUT_FILE]
```
#### Name File
Text file, with one line for each drum name. All drum names will be capitalised and padded to the correct length, and all non-alphanumeric character will be removed.

#### Audio File
Must be exactly 21504 samples long and use 8 bit signed samples in a headerless file.

A single file EXE is available on the [releases](https://github.com/mattybigback/SpecDrumTools/releases/) page.

## SpecDrum Clip Detector
SpecDrumClipDetector analyses the audio block and looks for potential clipping issues. The SpecDrum software uses a very simple summing algorithm for mixing samples together, so if samples are triggered together and they clip the result will be a nasty clicking sound as the sample wraps around.

Run from the command line/terminal, passing the file to be checked as an argument.


## XORFile
XORFile converts audio blocks to work with the AmDrum software. For some reason the developers XORed the audio with a text string. This script applies that process to SpecDrum audio blocks so they can be imported into AmDrum (you will need to add AMSDOS headers to both the header block and audio block to get them to import correctly).

