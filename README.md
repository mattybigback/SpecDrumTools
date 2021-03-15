# SpecDrumTools
Tools for making custom kits for the Cheetah SpecDrum

SpecDrum Clip Detector analyses the audio block and looks for potential clipping issues. The SpecDrum software uses a very simple summing algorithm for mixing samples together, so if samples are triggered together and they clip the result will be a nasty clicking sound as the sample wraps around.

Run from the command line/terminal, passing the file to be checked as an argument.
