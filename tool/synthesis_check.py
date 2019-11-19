"""Impulse responce generator check.

usage: synthesis_check.py [-h, --help] (-f <sampling_freq>) (-p <frame_period>) (-l <f0_lower>) (-i <interp_lf0_file>) (-s <spectrum_envelope_file>) (-a <aperiodicity_file>) (-o <outdir>) (-g <gpu_id>)

options:
  -h, --help                        Show this message and exit.
  -f <sampling_freq>                Sampling frequency in Hz (required).
  -p <frame_period>                 Frame period in millisecond (required).
  -l <f0_lower>                     Lower F0 limit in Hz (required).
  -i <interp_lf0_file>              Linear interpolated log-F0 binary file (required).
  -s <spectrum_envelope_file>       Spectrum envelope, binary file (required).
  -a <aperiodicity_file>            Aperiodicity, binary file (required).
  -o <outdir>                       Output directory for saving figure (required).
  -g <gpu_id>                       GPU ID; gpu_id<0: use cpu, gpu_id>=0: use gpu (required).
"""
from docopt import docopt

import numpy as np
from os.path import join, exists
import os
import sys

from scipy.io import wavfile

from worldmodify.pulse_train_generator import PulseGen
# from worldmodify.impulse_responce_generator_init_ver import ImpulseResponceGen
from worldmodify.impulse_responce_generator import ImpulseResponceGen

import pyworld
import torch

import time


def time_variant_filter_conv(x, h, gpu_id=-1):
    # x: input signal (excitation signal)
    # h: time variant filter
    #    - (T, N) array, T: time dim, N: impulse responce length
    out_len = x.shape[0] + h.shape[1] - 1
    output = np.zeros(out_len, dtype=np.float32)
    if gpu_id >= 0:
        output = torch.tensor(output,device='cuda:'+str(gpu_id))
    else:
        output = torch.tensor(output)
    h = h * x.reshape(-1, 1)
    for i in range(x.shape[0]):
        output[i:i+h.shape[1]] += h[i]
    return output

if __name__ == '__main__':
    args = docopt(__doc__)
    print("Command line args:\n", args)
    sampling_freq = int(args['-f'])
    frame_period = float(args['-p'])
    f0_lower = float(args['-l'])
    interp_lf0_file = args['-i']
    sp_file = args['-s']
    ap_file = args['-a']
    outdir = args['-o']
    gpu_id = int(args['-g'])
    
    for d in ['periodic', 'aperiodic', 'speech']:
        if not exists(join(outdir,d)):
            os.makedirs(join(outdir,d))
    
    fft_size = pyworld.get_cheaptrick_fft_size(sampling_freq, f0_lower)
    
    # ------------------- Pulse train generation ------------------------
    interp_lf0 = np.fromfile(interp_lf0_file, dtype=np.float32, sep="").reshape(-1)
    pulse_info = PulseGen(cont_f0=np.exp(interp_lf0), sampling_freq=sampling_freq, frame_period=frame_period)
    pulse_position = pulse_info.init_pulse_position()
    pulse_train = pulse_info.get_pulse_train(pulse_position) # ndarray
    if gpu_id >= 0:
        pulse_train = torch.tensor(pulse_train, requires_grad=True, device='cuda:'+str(gpu_id))
    else:
        pulse_train = torch.tensor(pulse_train, requires_grad=True)
    # -------------------------------------------------------------------
    
    # ------------------- White noise generation ------------------------
    noise_signal = np.random.normal(loc=0.,scale=1.,size=pulse_train.shape[0]).astype(np.float32 )
    if gpu_id >= 0:
        noise_signal = torch.tensor(noise_signal, device='cuda:'+str(gpu_id))
    else:
        noise_signal = torch.tensor(noise_signal)
    # -------------------------------------------------------------------
    
    # ------------------- Impulse responce generation --------------------------
    sp_numpy = np.fromfile(sp_file, dtype=np.float32, sep="").reshape(-1,fft_size//2+1)
    ap_numpy = np.fromfile(ap_file, dtype=np.float32, sep="").reshape(-1,fft_size//2+1)
    if gpu_id >= 0:
        sp_tensor = torch.tensor(sp_numpy, requires_grad=True, device='cuda:'+str(gpu_id))
        ap_tensor = torch.tensor(ap_numpy, requires_grad=True, device='cuda:'+str(gpu_id))
    else:
        sp_tensor = torch.tensor(sp_numpy, requires_grad=True)
        ap_tensor = torch.tensor(ap_numpy, requires_grad=True)
    responce_info = ImpulseResponceGen(sampling_freq=sampling_freq, frame_period=frame_period, fft_size=(sp_tensor.shape[1]-1)*2, gpu_id=gpu_id)
    periodic_responce, aperiodic_responce = responce_info.get_sample_level_responce(sp_tensor, ap_tensor)
    # --------------------------------------------------------------------------
    
    periodic_signal = time_variant_filter_conv(pulse_train, periodic_responce, gpu_id)
    aperiodic_signal = time_variant_filter_conv(noise_signal, aperiodic_responce, gpu_id)
    
    synthesis_signal = periodic_signal + aperiodic_signal
    
    if gpu_id >= 0:
        periodic_signal = periodic_signal.to('cpu')
        aperiodic_signal = aperiodic_signal.to('cpu')
    
    filename = os.path.splitext(os.path.basename(sp_file))[0]
    wavfile.write(join(outdir,'periodic',filename+'.wav'), sampling_freq, periodic_signal.data.numpy().astype(np.int16))
    wavfile.write(join(outdir,'aperiodic',filename+'.wav'), sampling_freq, aperiodic_signal.data.numpy().astype(np.int16))
    wavfile.write(join(outdir,'speech',filename+'.wav'), sampling_freq, synthesis_signal.cpu().data.numpy().astype(np.int16))
    
    # start = time.time()
    # print("start calculating gradient")
    # synthesis_signal[10000].backward()
    # end = time.time()
    # print('elapsed time: '+str(end-start))
    sys.exit(0)
