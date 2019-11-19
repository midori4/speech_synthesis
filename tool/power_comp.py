""" Compare power [dB] between natural speech and analysis-synthesis speech.

usage: power_comp.py [-h|--help] (-n <natural>) (-w <world_anasyn>) (-m <modified_anasyn>) (-o <outdir>)


options:
    -h, --help              Show this help message and exit.
    -n <natural>            Natural speech wav file (required).
    -w <world_anasyn>       Analysis-synthesis by WORLD wav file (required).
    -m <modified_anasyn>    Analysis-synthesis by modified version wav file (required).
    -o <outdir>             Output directory for natural speech (required).
"""
from docopt import docopt

import numpy as np
import matplotlib.pyplot as plt

from scipy.io import wavfile

from os.path import exists, join
import os

Vbase = 32768

def calc_power(data, num_frame, frame_period, frame_length):
  separated_waveform = np.array([data[i*frame_period:i*frame_period+frame_length].tolist() for i in range(num_frame)], dtype=np.float32)
  db_power_list = []
  for waveform in separated_waveform:
    power = np.mean(waveform**2)
    db_power = 10 * np.log10(power / Vbase**2)
    db_power_list.append(db_power)
  return np.array(db_power_list, dtype=np.float32)


if __name__ == '__main__':
  args = docopt(__doc__)
  print("Command line args:\n", args)
  natural_wavfile = args['-n']
  world_anasyn_wavfile = args['-w']
  modified_wavfile = args['-m']
  outdir = args['-o']
  for d in ['natural','world','modified_ver','svg','eps']:
    if not exists(join(outdir,d)):
      os.makedirs(join(outdir,d))
  
  frame_period = 5 # [ms]
  frame_length = 25 #[ms]
  
  fs, natural = wavfile.read(natural_wavfile)
  world = wavfile.read(world_anasyn_wavfile)[1]
  modified = wavfile.read(modified_wavfile)[1]
  
  frame_period = int(frame_period / 1000 * fs)
  frame_length = int(frame_length / 1000 * fs)
  # print(len(natural), len(world), len(modified))
  num_frame = int((len(natural) - frame_length) / frame_period)
  
  natural_power = calc_power(natural, num_frame, frame_period, frame_length)
  world_power = calc_power(world, num_frame, frame_period, frame_length)
  modified_power = calc_power(modified, num_frame, frame_period, frame_length)
  # save power as binary
  filename = os.path.splitext(os.path.basename(natural_wavfile))[0]
  natural_power.tofile(join(outdir,'natural',filename+'.power'))
  world_power.tofile(join(outdir,'world',filename+'.power'))
  modified_power.tofile(join(outdir,'modified_ver',filename+'.power'))

  # plot power for compare
  font_size = 24
  plt.figure(figsize=(11,7))
  plt.rcParams["font.size"] = font_size
  time_axis = np.arange(num_frame) * 5
  plt.plot(time_axis, natural_power, "k", linewidth=0.5, label="Original")
  plt.plot(time_axis, world_power, "b", linewidth=0.5, label="WORLD")
  plt.plot(time_axis, modified_power, "r", linewidth=0.5, label="Modified")
  plt.xlim(0, num_frame*5)
  plt.ylim(-85, 5)
  plt.xlabel("Time [ms]")
  plt.ylabel("Power [dB]")
  # plt.legend(bbox_to_anchor=(0.5, 0, 0.5, 1))
  plt.legend(loc='best', fontsize=20)
  plt.savefig(join(outdir,'svg',filename+'.svg'))
  plt.savefig(join(outdir,'eps',filename+'.eps'))
  # plt.show()
