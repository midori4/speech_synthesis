"""Impulse train generator check.

usage: pulse_train_check.py [-h, --help] (-i <interp_lf0_file>) (-o <outdir>)

options:
  -h, --help                Show this message and exit.
  -i <interp_lf0_file>      Linear interpolated log-F0 binary file (required).
  -o <outdir>               Output directory for saving figure (required).
"""
from docopt import docopt

import numpy as np
import os
from os.path import join, exists

from worldmodify.pulse_train_generator import PulseGen

import matplotlib.pyplot as plt

if __name__ == '__main__':
  args = docopt(__doc__)
  print("Command line args:\n", args)
  interp_lf0_file = args['-i']
  outdir = args['-o']
  interp_lf0 = np.fromfile(interp_lf0_file, dtype=np.float32, sep="").reshape(-1)
  pulse_info = PulseGen(cont_f0=np.exp(interp_lf0), sampling_freq=16000, frame_shift=5)
  pulse_position = pulse_info.init_pulse_position()
  pulse_train = pulse_info.get_pulse_train(pulse_position)
  
  if not exists(outdir):
    os.makedirs(outdir)
  plt.plot(pulse_train, "k", linewidth=0.2)
  plt.xlim(0,len(pulse_train)-1)
  plt.ylim(0,15)
  plt.savefig(join(outdir, "pulse_example.eps"))
  plt.savefig(join(outdir, "pulse_example.svg"))
 
  
