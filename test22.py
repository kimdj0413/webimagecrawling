# uniform
import random
import matplotlib.pyplot as plt

a = 0
b = 1
sample = [random.uniform(a,b) for _ in range(100000)]
print(len(sample))

plt.hist(sample, bins=50, edgecolor='black')
plt.show()
