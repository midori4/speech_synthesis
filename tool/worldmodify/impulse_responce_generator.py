import numpy as np
import torch

class ImpulseResponceGen:
  def __init__(self, sampling_freq, frame_period, fft_size, gpu_id=-1):
    self.sampling_freq = sampling_freq # [Hz]
    self.frame_period = int(self.sampling_freq * frame_period / 1000) # [sample]
    self.fft_size = fft_size
    
    self.my_safe_guard_constant = 1e-12
    self.gpu_id = gpu_id

  def to_sample_level(self, sp, ap):
    num_frame = sp.shape[0]
    num_sample = self.frame_period * (num_frame - 1)
    # from frame level to sample level by linear interpolation
    if self.gpu_id >= 0:
      W = torch.tensor([[1-i/self.frame_period,i/self.frame_period] for i in range(self.frame_period)], dtype=torch.float32, device='cuda:'+str(self.gpu_id))
      periodic = torch.empty((num_sample,sp.shape[1]),dtype=torch.float32,device='cuda:'+str(self.gpu_id))
      aperiodic = torch.empty((num_sample,ap.shape[1]),dtype=torch.float32,device='cuda:'+str(self.gpu_id))
    else:
      W = torch.tensor([[1-i/self.frame_period,i/self.frame_period] for i in range(self.frame_period)], dtype=torch.float32)
      periodic = torch.empty((num_sample,sp.shape[1]),dtype=torch.float32)
      aperiodic = torch.empty((num_sample,ap.shape[1]),dtype=torch.float32)
    for i in range(num_frame - 1):
      periodic[self.frame_period*i:self.frame_period*(i+1)] = torch.matmul(W, sp[i:i+2])
      aperiodic[self.frame_period*i:self.frame_period*(i+1)] = torch.matmul(W, ap[i:i+2])
    print("Interpolation finished!\n")
    return periodic, aperiodic
  
  def get_responce(self, log_sp):
    # Mirroring: size FFT_SIZE/2+1 -> FFT_SIZE
    tmp1 = np.eye(self.fft_size//2+1, dtype=np.float32).tolist()
    tmp2 = [[0.]*(self.fft_size//2-1-i)+[1.]+[0.]*(i+1) for i in range(self.fft_size//2-1)]
    W = torch.transpose(torch.tensor(tmp1+tmp2, dtype=torch.float32), 0, 1)
    if self.gpu_id >= 0:
      mirrored_sp = torch.matmul(log_sp, W.cuda('cuda:'+str(self.gpu_id)))
    else:
      mirrored_sp = torch.matmul(log_sp,W)
    print("Mirroring finished!\n")
    
    # cepstrum = ifft(log_sp) = fft(log_sp).conjugate()
    cepstrum = torch.rfft(mirrored_sp, signal_ndim=1, onesided=False)
    cepstrum[:,:,1] = cepstrum[:,:,1] * -1
    print("Calculation cepstrum finished!\n")
    
    # weighting
    half_fft_size = self.fft_size // 2
    cepstrum[:,1:half_fft_size] = 2. * cepstrum[:,1:half_fft_size]
    cepstrum[:,half_fft_size+1:] = 0.
    
    # ------------------ minimum phase spectrum calculation ------------------ #
    min_phase_sp = torch.fft(cepstrum, signal_ndim=1)
    
    # exp(x): minimum phase spectrum
    min_phase_sp[:,:,0], min_phase_sp[:,:,1] =\
      torch.exp(min_phase_sp[:,:,0]/self.fft_size) * torch.cos(min_phase_sp[:,:,1]/self.fft_size),\
      torch.exp(min_phase_sp[:,:,0]/self.fft_size) * torch.sin(min_phase_sp[:,:,1]/self.fft_size)
    print("Calculation minimum phase spectrum finished!\n")
    # ------------------ minimum phase spectrum calculation ------------------ #
    
    # minimum phase impulse responce calculation
    impulse_responce = torch.irfft(min_phase_sp[:,:half_fft_size+1], signal_ndim=1, onesided=True, signal_sizes=torch.Size([self.fft_size,]))
    return impulse_responce
  
  def get_sample_level_responce(self, sp, ap):
    periodic, aperiodic = self.to_sample_level(sp, ap)
    
    # calculation log-spectrum for periodic and aperiodic
    periodic, aperiodic =\
      torch.log((1 - aperiodic**2) * periodic + self.my_safe_guard_constant) / 2,\
      torch.log(aperiodic**2 * periodic + self.my_safe_guard_constant) / 2
    
    periodic_responce = self.get_responce(periodic)
    aperiodic_responce = self.get_responce(aperiodic)
    return periodic_responce, aperiodic_responce
