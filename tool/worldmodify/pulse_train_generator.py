import warnings

import numpy as np

class PulseGen:
  def __init__(self, cont_f0, sampling_freq, frame_period):
    self.cont_f0 = cont_f0 # frame level
    self.sampling_freq = sampling_freq # [Hz]
    self.frame_period = frame_period # [ms]
  
  def init_pulse_position(self):
    frame_period = int(self.sampling_freq * self.frame_period / 1000) # [sample]
    # The number of frames
    num_frame = len(self.cont_f0)
    # The number of samples
    num_sample = frame_period * (num_frame - 1)
    pulse_position = np.zeros(num_sample, dtype=np.int8)
    
    s = 0
    pulse_position[s] = 1
    tmp_f0 = self.cont_f0[s]
    while True:
      shift_width = int(1 / tmp_f0 * self.sampling_freq)
      s += shift_width
      if s >= num_sample:
        break
      pulse_position[s] = 1
      
      # calculate F0 at the s[sample] by linear interpolation
      previous_frame_ind = int(s / frame_period)
      following_frame_ind = previous_frame_ind + 1
      tmp_f0 = (self.cont_f0[following_frame_ind] - self.cont_f0[previous_frame_ind])\
                / frame_period * (s - previous_frame_ind * frame_period) + self.cont_f0[previous_frame_ind]
    return pulse_position
    
  # def update_pulse_position(self, impulse_train):
  
  
  def get_pulse_train(self, pulse_position):
    # pulse_train: for generation impulse train (amplitude-> sqrt(f_s/f_o))
    pulse_train = pulse_position.copy().astype(np.float32)
    pulse_position_ind = np.where(pulse_position == 1)[0]
    # The number of pulse 
    num_pulse = len(pulse_position_ind)
    if num_pulse == 1:
      warnings.warn("The number of pulse is {0}".format(str(num_pulse)))
    for i, pos in enumerate(pulse_position_ind):
      if i == 0:
        period = pulse_position_ind[i+1] # [sample]
        # Fo = 1/To = 1/(period[sample]/fs[Hz]) = fs/period -> Amp = sqrt(fs/Fo) = sqrt(period)
        pulse_train[pos] = np.sqrt(period)
      elif i == num_pulse - 1:
        period = pulse_position_ind[i] - pulse_position_ind[i-1]
        pulse_train[pos] = np.sqrt(period)
      else:
        # determined by average
        period = (pulse_position_ind[i+1] - pulse_position_ind[i-1]) / 2
        pulse_train[pos] = np.sqrt(period)
    return pulse_train
