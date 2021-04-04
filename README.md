# SpecDrumTools
Tools for making custom kits for the Cheetah SpecDrum

##SpecDrum Clip Detector
SpecDrumClipDetector analyses the audio block and looks for potential clipping issues. The SpecDrum software uses a very simple summing algorithm for mixing samples together, so if samples are triggered together and they clip the result will be a nasty clicking sound as the sample wraps around.

Run from the command line/terminal, passing the file to be checked as an argument.

##XORFile
XORFile converts audio blocks to work with the AmDrum software. For some reason the developers XORed the audio with a text string. This script applies that process to SpecDrum audio blocks so they can be imported into AmDrum (you will need to add AMSDOS headers to both the header block and audio block to get them to import correctly).
