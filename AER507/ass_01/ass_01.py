import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(10, 10000, 1000)
y = x * 1.6 * 10 ** (-16)
y = 6.7189 * 10 ** (-40) * np.exp(-5.602 * 10 ** (-7) / np.sqrt(y)) / y

plt.loglog(x, y, label='Model')
plt.legend()
plt.xlabel('Energy of Deterium')
plt.ylabel('Cross-section area')
plt.title('Cross-section area according to model')
plt.show()
