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
  if not exists(outdir):
    os.makedirs(outdir)
  
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
  
  #0 49
  #284 372
  #795
  sil_natural = natural_power.tolist()[0:50] + natural_power.tolist()[284:373] + natural_power.tolist()[795:]
  sil_world = world_power.tolist()[0:50] + world_power.tolist()[284:373] + world_power.tolist()[795:]
  sil_modified = modified_power.tolist()[0:50] + modified_power.tolist()[284:373] + modified_power.tolist()[795:]
  nosil_natural = natural_power.tolist()[49:284] + natural_power.tolist()[372:795]       
  nosil_world = world_power.tolist()[49:284] + world_power.tolist()[372:795]             
  nosil_modified = modified_power.tolist()[49:284] + modified_power.tolist()[372:795]    
                             
  world_rmse = np.sqrt(np.mean((np.array(sil_natural)-np.array(sil_world))**2))          
  modified_rmse = np.sqrt(np.mean((np.array(sil_natural)-np.array(sil_modified))**2))    
  print(world_rmse, modified_rmse)
  world_rmse = np.sqrt(np.mean((np.array(nosil_natural)-np.array(nosil_world))**2))      
  modified_rmse = np.sqrt(np.mean((np.array(nosil_natural)-np.array(nosil_modified))**2))
  print(world_rmse, modified_rmse)
