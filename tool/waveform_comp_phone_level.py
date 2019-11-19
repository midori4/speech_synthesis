""" plot waveform for checking the difference between natural speech and analysis-synthesis speech.

usage: waveform_comp_phone_level.py [-h|--help] (-n <natural>) (-w <world_anasyn>) (-m <modified_anasyn>) (-l <label>) (-o <outdir>)


options:
    -h, --help              Show this help message and exit.
    -n <natural>            Natural speech wav file (required).
    -w <world_anasyn>       Analysis-synthesis by WORLD wav file (required).
    -m <modified_anasyn>    Analysis-synthesis by modified version wav file (required).
    -l <label>              Triphone label file (required).
    -o <outdir>             Output directory for natural speech (required).
"""
from docopt import docopt

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

from os.path import exists, join
import os


args = docopt(__doc__)
print("Command line args:\n", args)

natural_speech_wavfile = args['-n']
world_anasyn_speech_wavfile = args['-w']
modified_anasyn_speech_wavfile = args['-m']
labfile = args['-l']
outdir = args['-o']

outdir_for_natural = join(outdir, "natural")
outdir_for_world = join(outdir, "world")
outdir_for_modified = join(outdir, "modified")

for outdir in [outdir_for_natural, outdir_for_world, outdir_for_modified]:
  if not exists(outdir):
    os.makedirs(outdir)

fs, natural = wavfile.read(natural_speech_wavfile)
world_anasyn = wavfile.read(world_anasyn_speech_wavfile)[1]
modified_anasyn = wavfile.read(modified_anasyn_speech_wavfile)[1]

with open(labfile, "r") as f:
    label = f.readlines()

label = [x.split(' ') for x in label]
# int(x) / 10000 -> [ms]
# [ms] / 1000 * fs -> the number of samples
label = [[int(int(x[0])/10000/1000.*fs), int(int(x[1])/10000/1000.*fs), x[2].split()[0]] for x in label]


for number, lab in enumerate(label):
    length = lab[1] - lab[0]
    
    font_size = 34
    x = np.linspace(0, float(length)/fs*1000, length)
    # -------- natural speech waveform plot ------------
    plt.figure(figsize=(11,7))
    plt.tick_params(labelbottom=False, bottom=False)
    plt.plot(x, natural[lab[0]:lab[1]], "k", linewidth=0.8)
    plt.rcParams["font.size"] = font_size
    # [samples] / (fs/1000) -> [ms]
    plt.xlim(0, length/16)
    plt.xlabel("Time",labelpad=10)
    plt.ylabel("Amplitude")
    plt.tight_layout()
    
    plt.savefig(join(outdir_for_natural, ('{:0>2}_'+lab[2]+'.svg').format(number)))
    plt.savefig(join(outdir_for_natural, ('{:0>2}_'+lab[2]+'.eps').format(number)))
    plt.close()
    
    # -------- analysis-synthesis by WORLD speech waveform plot ------------
    plt.figure(figsize=(11,7))
    plt.tick_params(labelbottom=False, bottom=False)
    plt.plot(x, world_anasyn[lab[0]:lab[1]], "k", linewidth=0.8)
    plt.rcParams["font.size"] = font_size
    # [samples] / (fs/1000) -> [ms]
    plt.xlim(0, length/16)
    plt.xlabel("Time",labelpad=10)
    plt.ylabel("Amplitude")
    plt.tight_layout()
    
    plt.savefig(join(outdir_for_world, ('{:0>2}_'+lab[2]+'.svg').format(number)))
    plt.savefig(join(outdir_for_world, ('{:0>2}_'+lab[2]+'.eps').format(number)))
    plt.close()
    
    # -------- analysis-synthesis by modified speech waveform plot ------------
    plt.figure(figsize=(11,7))
    plt.tick_params(labelbottom=False, bottom=False)
    plt.plot(x, modified_anasyn[lab[0]:lab[1]], "k", linewidth=0.8)
    plt.rcParams["font.size"] = font_size
    # [samples] / (fs/1000) -> [ms]
    plt.xlim(0, length/16)
    plt.xlabel("Time",labelpad=10)
    plt.ylabel("Amplitude")
    plt.tight_layout()
    
    plt.savefig(join(outdir_for_modified, ('{:0>2}_'+lab[2]+'.svg').format(number)))
    plt.savefig(join(outdir_for_modified, ('{:0>2}_'+lab[2]+'.eps').format(number)))
    plt.close()
