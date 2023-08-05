'''
Created on Mar 17, 2020

@author: hammonds
'''
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(30)
y = np.power(x, 2)

plt.ion()
plt.show()

plt.plot(x,y)

plt.draw()
plt.pause(5)