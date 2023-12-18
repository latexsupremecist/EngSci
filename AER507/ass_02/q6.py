import numpy as np

sigma = np.array([2e-29, 3e-28, 4e-28, 3e-28, 2e-28, 6e-29])
partition = np.array([[0, 40], [40, 60], [60, 100], [100, 140], [140, 300], [300, 2**31-1]])
mD = 3.343e-27
mT = 5.007e-27
mr = mD * mT / (mD + mT)
beta = mr / (2 * 8.617e-5 * 30 * 11606)
k = 2 * beta / mr
sum = 0
factor = 8 * np.power(beta, 1.5) * np.power(np.pi, -0.5) * np.sqrt(1.6e-16) / (mr ** 2)
for i in range(len(sigma)):
    [a, b] = partition[i]
    term = sigma[i] * factor * (np.exp(-k * a) * (k * a + 1) - np.exp(-k * b) * (k * b + 1)) / (k ** 2)
    print(f"{i+1}th term is {term}")
    sum += term

print(f"Sum is {sum}")
