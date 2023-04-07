import numpy as np

def linear(params, x):
    return params[0]*x + params[1]

features = [6.06, 0.12, 8.27, 10.74, 12.84 , 20.03]
avg1 = [4.82, 6.37, 10.62, 14.54]
avg2y = [7.27, 10.51]
avg2x = [3, 4]

# 7.27 = 3a + b
# 10.51 = 4a + b
# ----------------
# -3.24 = -a
# a = 3.24
# b = 7.27 - 3*3.24 
# b = -2.45

params = (3.24, -2.45)
print('params:', params)

x = np.array([7, 8, 15, 25, 100])
print(linear(params, x))

real = np.array(linear(params, x))
measured = np.array([23.97, 27.54, 72.19, 79.01, 251.57])

print('relativne odchylky:', np.abs(measured - real)/real)
print('zamietame 72.19 a 251.57 lebo ich relativna odchylka > 20%')


