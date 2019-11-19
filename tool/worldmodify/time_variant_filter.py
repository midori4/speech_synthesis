import pytorch

def conv(x, h, gpu_id=-1):
  # x: input signal (excitation signal)
  # h: time variant filter
  #    - (T, N) array, T: time dim, N: impulse responce length
  out_len = x.shape[0] + h.shape[1] - 1
  conv_matrix = torch.zeros((out_len,x.shape[0]), dtype=torch.float32)
  if gpu_id >= 0:
    conv_matrix = torch.zeros((out_len,x.shape[0]), dtype=torch.float32, device='cuda:'+str(gpu_id))
  else:
    conv_matrix = torch.zeros((out_len,x.shape[0]), dtype=torch.float32)
  filtered_series = torch.matmul(
  return output


