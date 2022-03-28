import matplotlib.pyplot as plt
import numpy as np


data = np.genfromtxt('acceleration_mouvement.csv',delimiter=',', skip_header=1)

acc_x = data[:, 0]
acc_y = data[:, 1]
acc_z = data[:, 2]
mag_x = data[:, 3]
mag_y = data[:, 4]
mag_z = data[:, 5]
gyro_x = data[:, 6]
gyro_y = data[:, 7]
gyro_z = data[:, 8]


limit = 18


temps = np.arange(0, 100/5, 0.2)
threshold = np.ones(100)*limit
plt.plot(temps, acc_x[0:100])
plt.show()

norme_acc = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
plt.plot(temps, norme_acc[0:100])
plt.plot(temps, threshold)
plt.show()

state = 0
fail = 0
for element in norme_acc:
    if element >= limit and state == 0:
        fail += 1
        state = 1

    if element < limit:
        state = 0


print("Limite dépassée ", fail, " fois.")