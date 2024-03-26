import numpy as np


def print_complex(num, text):
    formatted_real = "{:.3g}".format(num.real)
    formatted_imag = "{:.3g}".format(num.imag)
    sign = '-' if num.imag < 0 else '+'
    if formatted_imag[0] == '-':
        formatted_imag = formatted_imag[1:]
    print(f"{text} = {formatted_real} {sign} j{formatted_imag}")


def rotate(zl, length):
    return (zl + np.tan(2*np.pi*length)*1j) / (1 + zl * np.tan(2*np.pi*length)*1j)


def im_load(b, wl=37.5):
    angle = np.arctan(-1/b)/(2*np.pi)
    if angle < 0:
        angle += 0.5
    return wl * angle


def impedances(Zl, z0=50):
    zl = Zl/z0
    zlA = rotate(zl, 3.4/37.5)
    print_complex(zlA, "zlA")
    ylA = 1/zlA
    print_complex(ylA, "ylA")
    b1 = 0.05 - ylA.imag
    print(f"b1 = {b1}")
    ylB = ylA.real + 0.05j
    zlB = 1/ylB
    zlC = rotate(zlB, 3.8/37.5)
    ylC = 1/zlC
    print_complex(ylC, "ylC")
    b2 = -0.139
    print(f"b2 = {b2}")
    ylin = ylC + b2*1j
    print_complex(ylin, "ylin")
    print(f"Lengths are {im_load(b1)} and {im_load(b2)}")


impedances(complex(30.3, 6.85))

# B2 is probably wrong, l2 = 8.55
