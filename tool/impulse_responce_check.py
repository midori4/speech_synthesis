"""Impulse responce generator check.

usage: impulse_responce_check.py [-h, --help] (-s <spectrum_envelope_file>) (-a <aperiodicity_file>) (-o <outdir>) (-g <gpu_id>)

options:
  -h, --help                        Show this message and exit.
  -s <spectrum_envelope_file>       Spectrum envelope, binary file (required).
  -a <aperiodicity_file>            Aperiodicity, binary file (required).
  -o <outdir>                       Output directory for saving figure (required).
  -g <gpu_id>                       GPU ID; gpu_id<0: use CPU, gpu_id>=0: use GPU (required).
"""
from docopt import docopt

import numpy as np
import os
from os.path import join, exists
import sys

from worldmodify.impulse_responce_generator import ImpulseResponceGen

import torch

if __name__ == '__main__':
  args = docopt(__doc__)
  print("Command line args:\n", args)
  sp_file = args['-s']
  ap_file = args['-a']
  outdir = args['-o']
  gpu_id = int(args['-g'])
  
  fft_size = 1024
  sp_numpy = np.fromfile(sp_file, dtype=np.float32, sep="").reshape(-1,fft_size//2+1)
  ap_numpy = np.fromfile(ap_file, dtype=np.float32, sep="").reshape(-1,fft_size//2+1)
  if gpu_id >= 0:
    sp_tensor = torch.tensor(sp_numpy, requires_grad=True, device='cuda:'+str(gpu_id))
  else:
    sp_tensor = torch.tensor(sp_numpy, requires_grad=True)
  if gpu_id >= 0:
    ap_tensor = torch.tensor(ap_numpy, requires_grad=True, device='cuda:'+str(gpu_id))
  else:
    ap_tensor = torch.tensor(ap_numpy, requires_grad=True)
  responce_info = ImpulseResponceGen(sampling_freq=16000, frame_shift=5, fft_size=(sp_numpy.shape[1]-1)*2, gpu_id=gpu_id)
  # responce_info = ImpulseResponceGen(sp_tensor, ap_tensor, sampling_freq=16000, frame_shift=5, gpu_id=gpu_id)
  periodic_responce, aperiodic_responce = responce_info.get_sample_level_responce(sp_tensor,ap_tensor)
  # periodic_responce, aperiodic_responce = responce_info.get_sample_level_responce()
  print("start auto-differentiation")
  periodic_responce[5000][10].backward()
  print("end auto-differentiation")
  if not exists(outdir):
    os.makedirs(outdir)
  periodic_responce.to('cpu').data.numpy().tofile(join(outdir, 'periodic.ir'))
  aperiodic_responce.to('cpu').data.numpy().tofile(join(outdir, 'aperiodic.ir'))
  sys.exit(0)
