import numpy as np
import torch

class ImpulseResponceGen:
  def __init__(self, sampling_freq, frame_shift, fft_size, gpu_id=-1):
    self.sampling_freq = sampling_freq # [Hz]
    self.frame_shift = frame_shift # [ms]
    self.frame_period = int(self.sampling_freq * self.frame_shift / 1000) # [sample]
    self.fft_size = fft_size
    
    self.my_safe_guard_constant = 1e-12
    self.gpu_id = gpu_id
    
  def to_sample_level(self, sp, ap):
    # The number of frames
    num_frame = sp.shape[0]
    num_sample = self.frame_period * (num_frame - 1)
    
    # prepare matrix for interpolation
    tmp = torch.tensor([[1-i/self.frame_period,i/self.frame_period] for i in range(self.frame_period)], dtype=torch.float32)
    W = torch.zeros((num_sample,num_frame), dtype=torch.float32)
    for i in range(num_frame-1):
      W[self.frame_period*i:self.frame_period*(i+1),i:i+2] = tmp
    if self.gpu_id >= 0:
     sample_level_sp = torch.matmul(W.cuda('cuda:'+str(self.gpu_id)), sp) # sample level
     sample_level_ap = torch.matmul(W.cuda('cuda:'+str(self.gpu_id)), ap) # sample level
    else:
      sample_level_sp = torch.matmul(W, sp) # sample level
      sample_level_ap = torch.matmul(W, ap) # sample level
    print("Interpolation finished!\n")
    return sample_level_sp, sample_level_ap
  
  def mirroring(self, log_sp):
    # Mirroring: size FFT_SIZE/2+1 -> FFT_SIZE
    tmp1 = np.eye(self.fft_size//2+1, dtype=np.float32).tolist()
    tmp2 = [[0.]*(self.fft_size//2-1-i)+[1.]+[0.]*(i+1) for i in range(self.fft_size//2-1)]
    W = torch.transpose(torch.tensor(tmp1+tmp2, dtype=torch.float32), 0, 1)
    if self.gpu_id >= 0:
      mirrored_sp = torch.matmul(log_sp, W.cuda('cuda:'+str(self.gpu_id)))
    else:
      mirrored_sp = torch.matmul(log_sp, W)
    print("Mirroring finished!\n")
    return mirrored_sp
  
  def to_cepstrum(self, x):
    # cepstrum = ifft(log_sp) = fft(log_sp).conjugate()
    W = torch.tensor([[1,0],[0,-1]], dtype=torch.float32) # for conversion to complex conjugate
    if self.gpu_id >= 0:
      cepstrum = torch.matmul(torch.rfft(x, signal_ndim=1, onesided=False), W.cuda('cuda:'+str(self.gpu_id)))
    else:
      cepstrum = torch.matmul(torch.rfft(x, signal_ndim=1, onesided=False), W)
    print("Calculation cepstrum finished!\n")
    return cepstrum
  
  def weighting(self, x):
    # W = [[1.] + [0.] * (self.fft_size - 1)]\
    #       + [[0.]*(i+1)+[2.]+[0.]*(self.fft_size-2-i) for i in range(self.fft_size//2-1)]\
    #       + [[0.]*(self.fft_size//2)+[1.]+[0.]*(self.fft_size//2-1)]\
    #       + [[0.]*self.fft_size]*(self.fft_size//2-1)
    # W = np.array(W, dtype=np.float32)
    # return torch.matmul(torch.tensor(W),x)
    
    # if self.gpu_id >= 0:
    #   weighted_x = torch.zeros(x.shape, dtype=torch.float32, device='cuda:'+str(self.gpu_id))
    # else:
    #    weighted_x = torch.zeros(x.shape, dtype=torch.float32)
    # half_fft_size = self.fft_size // 2
    # weighted_x[:,0] = x[:,0]
    # weighted_x[:,1:half_fft_size] = 2. * x[:,1:half_fft_size]
    # weighted_x[:,half_fft_size] = x[:,half_fft_size]
    half_fft_size = self.fft_size // 2
    x[:,1:half_fft_size] = 2. * x[:,1:half_fft_size]
    x[:,half_fft_size+1:] = 0.
    return x

  def to_min_phase_spectrum(self, x):
    tmp = torch.fft(x, signal_ndim=1)
    dim = self.fft_size // 2 + 1
    # exp(x): minimum phase spectrum
    if self.gpu_id >= 0:
      min_phase_spectrum = torch.zeros((x.shape[0],dim,2),dtype=torch.float32,device='cuda:'+str(self.gpu_id))
    else:
      min_phase_spectrum = torch.zeros((x.shape[0],dim,2),dtype=torch.float32)
    min_phase_spectrum[:,:,0], min_phase_spectrum[:,:,1] =\
      torch.exp(tmp[:,:dim,0]/self.fft_size) * torch.cos(tmp[:,:dim,1]/self.fft_size),\
      torch.exp(tmp[:,:dim,0]/self.fft_size) * torch.sin(tmp[:,:dim,1]/self.fft_size)
    print("Calculation minimum phase spectrum finished!\n")
    return min_phase_spectrum
  
  def to_impulse_responce(self, x):
    return torch.irfft(x, signal_ndim=1, onesided=True, signal_sizes=torch.Size([self.fft_size,]))
  
  def get_impulse_responce(self, log_sp):
    return self.to_impulse_responce(\
            self.to_min_phase_spectrum(\
            self.weighting(\
            self.to_cepstrum(\
            self.mirroring(log_sp)))))
  
  def get_sample_level_responce(self, sp, ap):
    sample_level_sp, sample_level_ap = self.to_sample_level(sp, ap)
    periodic_log_sp = torch.log((1 - sample_level_ap**2) * sample_level_sp + self.my_safe_guard_constant) / 2
    aperiodic_log_sp = torch.log(sample_level_ap**2 * sample_level_sp + self.my_safe_guard_constant) / 2
    periodic_responce = self.get_impulse_responce(periodic_log_sp)
    aperiodic_responce = self.get_impulse_responce(aperiodic_log_sp)
    return periodic_responce, aperiodic_responce
