import numpy as np
import time

from pykeops.numpy import LazyTensor as LazyTensor_np
from pykeops.torch import LazyTensor as LazyTensor_torch
import cupy as cp
import torch
from torch.utils.dlpack import to_dlpack, from_dlpack

# Function:
def direct_pykeops_compute_torch(points, epsilon=1e-5, do_reshape=True):
    eps = torch.FloatTensor([(epsilon ** 2)]).to("cuda")
    weights = cp.hstack([cp.ones((points.shape[0], 1), dtype=np.float32), points])
    weights = from_dlpack(weights.toDlpack())
    x_i = LazyTensor_torch(weights[:, None, :])
    y_j = LazyTensor_torch(weights[None, :, :])
    kernel_ij = x_i * (((x_i[1:] - y_j[1:])**2).sum(-1) + eps).rsqrt()
    # kernel_ij = (-((x_i[1:] - y_j[1:])**2).sum(-1) / eps).exp()
    # kernel_ij = x_i / (((x_i - y_j)*(x_i - y_j)).sum(-1) + eps)
    cupy_return_array = cp.fromDlpack(to_dlpack(kernel_ij.sum(0)))
    if do_reshape:
        return cp.reshape(cupy_return_array, cupy_return_array.size, order='F')
    else:
        return cupy_return_array


# Benchmark Test function:
start_N = 100
stop_N = 1e5
num_iterations = 10
num_N = 10

times_GPU = []
all_N = np.geomspace( start_N, stop_N, num_N).astype('int')
for N in all_N:
    print(N)
    time_GPU = 0
    for i in range(num_iterations):
        print(i)
        points = cp.random.random((N, 3), dtype=np.float32)
        st = time.time()
        pots = direct_pykeops_compute_torch(points)
        tiime = (time.time() - st)
        print(tiime)
        time_GPU += tiime / num_iterations
    times_GPU.append(time_GPU)
print(all_N)
print(times_GPU)


