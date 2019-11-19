""" plot waveform for checking the difference between natural speech and analysis-synthesis speech.

usage: mkfig_waveform_comp_for_document.py [-h|--help] (-n <natural>) (-w <world_anasyn>) (-m <modified_anasyn>) (-l <label>) (-o <outdir>)


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
import matplotlib
matplotlib.use('Agg')
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

left_label = 'm-a+g'
middle_label = 'u-r+u'
right_label = 'i-b+u'

font_size = 18
fig = plt.figure(figsize=(13,6))
plt.rcParams["font.size"] = font_size
for lab in label:
  if lab[2] == left_label:
    font_size = 18
    fig = plt.figure(figsize=(13,6))
    plt.rcParams["font.size"] = font_size
    length = lab[1] - lab[0]
    x = np.linspace(0, float(length)/fs*1000, length)

    # -------- natural speech waveform plot ------------
    ax1 = fig.add_subplot(311)
    ax1.tick_params(labelbottom=False, bottom=False)
    ax1.plot(x, natural[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax1.set_xlim(0, length/16)
    ax1.set_ylim(-6700,14000)
    ax1.set_ylabel("Amplitude")
    
    # -------- analysis-synthesis by WORLD speech waveform plot ------------
    ax4 = fig.add_subplot(312)
    ax4.tick_params(labelbottom=False, bottom=False)
    ax4.plot(x, world_anasyn[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax4.set_xlim(0, length/16)
    ax4.set_ylim(-6700,14000)
    ax4.set_ylabel("Amplitude")
    
    # -------- analysis-synthesis by modified speech waveform plot ------------
    ax7 = fig.add_subplot(313)
    ax7.tick_params(labelbottom=False, bottom=False)
    ax7.plot(x, modified_anasyn[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax7.set_xlim(0, length/16)
    ax7.set_ylim(-6700,14000)
    ax7.set_xlabel("Time",labelpad=9)
    ax7.set_ylabel("Amplitude")
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.34)
    plt.savefig(join(outdir, lab[2]+'.svg'))
    plt.savefig(join(outdir, lab[2]+'.eps'))
    plt.close()
  elif lab[2] == middle_label:
    font_size = 18
    fig = plt.figure(figsize=(13,6))
    plt.rcParams["font.size"] = font_size
    length = lab[1] - lab[0]
    x = np.linspace(0, float(length)/fs*1000, length)

    # -------- natural speech waveform plot ------------
    ax2 = fig.add_subplot(311)
    ax2.tick_params(labelbottom=False, bottom=False)
    ax2.plot(x, natural[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax2.set_xlim(0, length/16)
    ax2.set_ylim(-6700,7000)
    
    # -------- analysis-synthesis by WORLD speech waveform plot ------------
    ax5 = fig.add_subplot(312)
    ax5.tick_params(labelbottom=False, bottom=False)
    ax5.plot(x, world_anasyn[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax5.set_xlim(0, length/16)
    ax5.set_ylim(-6700,7000)
    
    # -------- analysis-synthesis by modified speech waveform plot ------------
    ax8 = fig.add_subplot(313)
    ax8.tick_params(labelbottom=False, bottom=False)
    ax8.plot(x, modified_anasyn[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax8.set_xlabel("Time",labelpad=9)
    ax8.set_xlim(0, length/16)
    ax8.set_ylim(-6700,7000)
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.34)
    plt.savefig(join(outdir, lab[2]+'.svg'))
    plt.savefig(join(outdir, lab[2]+'.eps'))
    plt.close()
    
  elif lab[2] == right_label:
    font_size = 18
    fig = plt.figure(figsize=(13,6))
    plt.rcParams["font.size"] = font_size
    length = lab[1] - lab[0]
    x = np.linspace(0, float(length)/fs*1000, length)

    # -------- natural speech waveform plot ------------
    ax3 = fig.add_subplot(311)
    ax3.tick_params(labelbottom=False, bottom=False)
    ax3.plot(x, natural[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax3.set_xlim(0, length/16)
    ax3.set_ylim(-1800,3600)
   
    # -------- analysis-synthesis by WORLD speech waveform plot ------------
    ax6 = fig.add_subplot(312)
    ax6.tick_params(labelbottom=False, bottom=False)
    ax6.plot(x, world_anasyn[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax6.set_xlim(0, length/16)
    ax6.set_ylim(-1800,3600)
   
    # -------- analysis-synthesis by modified speech waveform plot ------------
    ax9 = fig.add_subplot(313)
    ax9.tick_params(labelbottom=False, bottom=False)
    ax9.plot(x, modified_anasyn[lab[0]:lab[1]], "k", linewidth=0.5)
    # [samples] / (fs/1000) -> [ms]
    ax9.set_xlim(0, length/16)
    ax9.set_xlabel("Time",labelpad=9)
    ax9.set_ylim(-1800,3600)
    fig.tight_layout()
    fig.subplots_adjust(wspace=0.34)
    plt.savefig(join(outdir, lab[2]+'.svg'))
    plt.savefig(join(outdir, lab[2]+'.eps'))
    plt.close()
 
