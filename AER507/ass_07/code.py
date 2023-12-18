import numpy as np
import matplotlib.pyplot as plt


def q2a(sv):
    k = 1
    T = 1
    m = 1
    ngd = 4 * np.sqrt(k*T/m) / sv
    return ngd


def q2():
    #temp = np.array([2, 3, 4, 5, 7, 10, 20, 30, 40, 50, 70, 100])
    #sigma = np.array([1e-17, 1e-16, 4e-16, 1e-15, 3e-15, 6e-15, 2.5e-14, 3e-14, 4e-14, 4.5e-14, 5e-14, 5e-14])
    c2 = np.loadtxt("3c2.csv", delimiter=',')
    temp = c2[:, 0]
    sviz = c2[:, 1]
    sviz *= 1e-17
    cs = np.sqrt(1.602e-19 * temp / (2.016e-3 / 6.02e23))
    ngd = 4 * cs / sviz
    plt.loglog(temp, ngd, label='curve')
    coll = np.sqrt(temp / (sviz * 3.78e-24))
    plt.loglog(temp, coll, label='collisional')
    b2 = np.loadtxt("3b2.csv", delimiter=',')
    temp = b2[:, 0]
    sen = b2[:, 1]
    sen *= 1e-20
    plt.loglog(temp, 2 / sen, label='validity')
    plt.title('n_gd against T_e')
    plt.xlabel('Temperature (eV)')
    plt.ylabel('n_gd (m^-2)')
    plt.legend()
    plt.show()


def q5(lis):
    [I, R, a, k, n, B, A, P] = lis
    tau = 0.048 * np.power(I, 0.85) * np.power(R, 1.2) * np.power(a, 0.3) * np.power(k, 0.5) * np.power(n, 0.1) * np.power(B, 0.2) * np.power(A, 0.5) / np.power(P, 0.5)
    nG = I / (np.pi * a ** 2)
    lawson = tau * nG
    print(f"tau is {tau}\nnG is {nG}\nLawson is {lawson}")
    return


jt = []
