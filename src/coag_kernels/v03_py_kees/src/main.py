import sys

import numpy as np
# import matplotlib.pyplot as plt

from config import Config
import utils
from utils.cprint import cprint

run_id = sys.argv[1]
cfg = Config()
cprint(f"{run_id}", indent=1, color="cyan")

n = 100
mmin = 10**cfg.mass_grid_exp_min
mmax = 10**cfg.mass_grid_exp_max
m = mmin * (mmax/mmin)**np.linspace(0, 1, n)
msum = m[:, None] + m[None, :]
kk_l = np.interp(msum, m, np.arange(n))
kk_l = np.array(kk_l, dtype=int)
kk_h = kk_l+1
# One more than necessary (useful for indexing)
mm = np.hstack((m, [m[-1]**2/m[-2]]))
eeps = (msum-m[kk_l])/(mm[kk_h]-m[kk_l])

K_kij = np.zeros((n, n, n))
K_kij_nc = np.zeros((n, n, n))
f_gain = np.ones((n, n))
for i in range(n):
    f_gain[i, i+1:] = 0
    f_gain[i, i] = 0.5

R_kij = 1.

for i in range(n):
    for j in range(n):
        k_l = kk_l[i, j]
        k_h = kk_h[i, j]
        eps = eeps[i, j]
        # ^ NOTE: second case of near-zero-cancellation here, needs fix!

        # First the normal version
        K_kij[i, i, j] -= R_kij
        K_kij[k_l, i, j] += f_gain[i, j]*R_kij*(1-eps)
        if k_h < n:
            K_kij[k_h, i, j] += f_gain[i, j]*R_kij*eps

        # Now the near cancellation version
        if k_l > i:
            K_kij_nc[i, i, j] -= R_kij
            K_kij_nc[k_l, i, j] += f_gain[i, j]*R_kij*(1-eps)
            if k_h < n:
                K_kij_nc[k_h, i, j] += f_gain[i, j]*R_kij*eps
        elif k_l == max(i, j):
            K_kij_nc[k_l, i, j] -= f_gain[i, j]*R_kij*eps
            if k_h < n:
                K_kij_nc[k_h, i, j] += f_gain[i, j]*R_kij*eps
            if i == j:
                K_kij_nc[k_l, i, j] -= 1/2 * R_kij   # NOTE no eps here

k = n//2

# plt.figure()
# plt.imshow(K_kij[k],origin='lower')

# plt.figure()
# plt.imshow(K_kij_nc[k],origin='lower')

# plt.show()

print(K_kij_nc[50, 50, :])

utils.file_io.save_coagulation_kernel_to_file(cfg, run_id, K_kij_nc)
