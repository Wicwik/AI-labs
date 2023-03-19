import numpy as np

p = np.array([0.9, 0.95, 0.98])

def calculate_confidence_interval(z, mean, std_dev, n):
    return (mean - z*(std_dev/np.sqrt(n)), mean + z*(std_dev/np.sqrt(n)))

def calculate_alpha_half(p):
    return (1 - p)/2


for pp in p:
    print(calculate_alpha_half(pp))

# p = 0.9 -> alpha/2 = 0.05
# p = 0.95 -> alpha/2 = 0.025
# p = 0.9 -> alpha/2 = 0.01 

mean = 3.744
std_dev = 1.799
n = 100
z = [-1.64, -1.96, -2.33]

for zz in z:
    print(calculate_confidence_interval(zz, mean, std_dev, n))

