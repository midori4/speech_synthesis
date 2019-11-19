""" plot F0 contour for checking the difference between natural speech and analysis-synthesis speech.

usage: f0_comp.py [-h|--help] (-n <natural_lf0_file>) (-w <world_lf0_file>) (-m <modified_lf0_file>) (-o <outdir>)


options:
    -h, --help              Show this help message and exit.
    -n <natural>            Log F0 of Natural speech (required).
    -w <world_anasyn>       Log F0 of analysis-synthesis speech by WORLD (required).
    -m <modified_anasyn>    Log F0 of analysis-synthesis speech by modified version (required).
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

import pyworld
import pyreaper


args = docopt(__doc__)
print("Command line args:\n", args)

natural_lf0_file = args['-n']
world_lf0_file = args['-w']
modified_lf0_file = args['-m']
outdir = args['-o']
for d in ['svg', 'eps']:
  if not exists(join(outdir,d)):
    os.makedirs(join(outdir,d))

natural_lf0 = np.fromfile(natural_lf0_file, dtype=np.float32, sep="").reshape(-1)
world_lf0 = np.fromfile(world_lf0_file, dtype=np.float32, sep="").reshape(-1)
modified_lf0 = np.fromfile(modified_lf0_file, dtype=np.float32, sep="").reshape(-1)

font_size = 24
fig = plt.figure(figsize=(11,7))
plt.rcParams["font.size"] = font_size
length = len(natural_lf0)

frame_period = 5.0
x = np.linspace(0, length*frame_period, length)
# -------- natural speech waveform plot ------------
plt.plot(x, natural_lf0, "k", linewidth=0.5, label="Original")
plt.plot(x, world_lf0[:length], "b", linewidth=0.5, label="WORLD")
plt.plot(x, modified_lf0[:length], "r", linewidth=0.5, label="Modified")
# [samples] / (fs/1000) -> [ms]
plt.xlim(0, length*frame_period)
plt.ylim(4.2, 5.45)
plt.ylabel("log F0")
plt.xlabel("time [ms]")
plt.legend(loc='best', fontsize=20)   
fig.tight_layout()

filename = os.path.splitext(os.path.basename(natural_lf0_file))[0]
plt.savefig(join(outdir,'svg',filename+'.svg'))
plt.savefig(join(outdir,'eps',filename+'.eps'))
plt.close() 
# -------------------------------------------------
