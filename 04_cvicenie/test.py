# generate random points in a circle

import numpy as np 
import pylab as plt 


num_samples = 1000

# make a simple unit circle 
theta = np.linspace(0, 2*np.pi, num_samples)
a, b = 5 * np.cos(theta), 5 * np.sin(theta)

# generate the points
# theta = np.random.rand((num_samples)) * (2 * np.pi)
r = np.random.uniform(0, 5, num_samples)
x, y = r * np.cos(theta), r * np.sin(theta)

# plots
plt.figure(figsize=(7,6))
plt.plot(a, b, linestyle='-', linewidth=2, label='Circle')
plt.plot(x, y, marker='o', linestyle=' ', label='Samples')
plt.ylim([-5.5,5.5])
plt.xlim([-5.5,5.5])
plt.grid()
plt.legend(loc='upper right')
plt.show(block=True)