""" Checks SpecDrum audio blocks for clipping (integer overflow) """
import sys
from argparse import ArgumentParser
from lib import libtzxtools as tzx


group1Sample1 = bytearray()
group2Sample1 = bytearray()
group2Sample2 = bytearray()
group2Sample3 = bytearray()
group3Sample1 = bytearray()
group3Sample2 = bytearray()
group3Sample3 = bytearray()
group3Sample4 = bytearray()
group_samples = [[group2Sample1, 3072],
                 [group2Sample2, 3072],
                 [group2Sample3, 3072],
                 [group3Sample1, 2048],
                 [group3Sample2, 2048],
                 [group3Sample3, 3072],
                 [group3Sample4, 3072],
                 [group1Sample1, 2048]]

drum_names = ["group1Sample1",
              "group2Sample1",
              "group2Sample2",
              "group2Sample3",
              "group3Sample1",
              "group3Sample2",
              "group3Sample3",
              "group3Sample4"]

parser = ArgumentParser()
parser.add_argument("fileName", help="Open specified file")
args = parser.parse_args()
audio_block_path = args.fileName

if audio_block_path is None:
    print("No input file specified. Please specify a file")
    sys.exit()

tzx.verify_file(audio_block_path, "audio")
group_samples = tzx.assign_samples(audio_block_path, group_samples)

for sample1 in group_samples[0:3]:
    for sample2 in group_samples[4:7]:
        for i, drum_name in enumerate(drum_names[1:4]):
            clip_count = 0
            clip_count += tzx.detect_clips(group_samples[7][0], sample1[0], sample2[0], drum_names[0].strip(), drum_name.strip(), drum_names[i+4].strip())
print("{} clips found".format(clip_count))
