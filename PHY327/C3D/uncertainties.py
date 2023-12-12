import numpy as np


def unc_rho1(v, a, b, i, dv, da, db, di):
    v_term = dv * a / (b * i)
    a_term = da * v / (b * i)
    b_term = v * a * db / (b ** 2 * i)
    i_term = v * a * di / (i ** 2 * b)
    return np.sqrt(v_term ** 2 + a_term ** 2 + b_term ** 2 + i_term ** 2)


def unc_rho2(v, a, b, i=1, dv=0.0005, da=0.1, db=0.1, di=0.025):
    k = 2 * np.pi * 0.016e-6
    v_term = k * a * dv / (b * i)
    a_term = k * da * v / (b * i)
    b_term = k * a * v * db / (b ** 2 * i)
    i_term = k * a * v * di / (b * i ** 2)
    return np.sqrt(v_term ** 2 + a_term ** 2 + b_term ** 2 + i_term ** 2)


a = 1.3e-2 * 0.016e-3
da = 0.1e-2 * 0.016e-3

ans1 = unc_rho1(1.89e-3, a, 1e-2, 1, 0.005e-3, da, 0.1e-2, 0.025)
# print(f"Uncertainty is {ans}")
ans2 = unc_rho2(0.083, 5, 0.5)
print(f"Uncertainty is {ans2}")
