import cv2
import os
import numpy as np
from scipy.fftpack import fft2, fftshift


# Does not work; used manual counting instead
def k_image(image_path, static_path):
    # Read the grayscale image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    static = cv2.imread(static_path, cv2.IMREAD_GRAYSCALE)

    # Subtract background from image
    img -= static

    # View image
    # poor image quality makes it impossible to analyse using code
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Apply Fourier Transform
    f_transform = fft2(img)
    f_transform_shifted = fftshift(f_transform)

    # Calculate magnitude spectrum
    magnitude_spectrum = np.abs(f_transform_shifted)

    # Find the peak in the magnitude spectrum
    max_val = np.max(magnitude_spectrum)
    max_loc = np.where(magnitude_spectrum == max_val)

    # Calculate the wave vector magnitude
    rows, cols = img.shape
    center_row, center_col = rows // 2, cols // 2
    wave_vector_magnitude = np.sqrt((max_loc[0][0] - center_row)**2 + (max_loc[1][0] - center_col)**2)

    return wave_vector_magnitude


def k_batch(path):
    lis = []
    for file in os.listdir(path):
        if file != "static.png":
            lis.append(k_image(path + file, path + "static.png"))
    return lis


def instability(k, dk, gamma, rho, h, dh, vpp, dvpp, eta, g=9.81):
    omega_0 = np.sqrt(k * (g + gamma * k ** 2 / rho) * np.tanh(k * h))
    k_term = dk * ((3 * k ** 2 * gamma / rho + g) * np.tanh(k * h) + k * (g + gamma * k ** 2 / rho) * (1 - np.tanh(k * h) ** 2) * h)
    h_term = dh * k * (g + gamma * k ** 2 / rho) * (1 - np.tanh(k * h)) * k
    domega_0 = (0.5 / omega_0) * np.sqrt(k_term ** 2 + h_term ** 2)
    Gamma = 2 * vpp
    dGamma = 2 * dvpp
    delta = np.sqrt((Gamma * omega_0 / 2) ** 2 - (4 * eta * k ** 2 / rho) ** 2)
    g_term = Gamma * dGamma * omega_0 ** 2 / 2
    o_term = omega_0 * domega_0 * Gamma ** 2 / 2
    ddelta = 0.5 / delta * np.sqrt(g_term ** 2 + o_term ** 2)
    return ((2 * omega_0, delta), (np.sqrt(4 * domega_0 ** 2 + ddelta ** 2)))


def inst_water(m, n, h, vpp, dh=0.005, dvpp=0.125e-3, r=9.75e-2, dr=0.025e-2):
    k = m * np.sqrt(1 + n ** 2) / r
    dk = k * dr / r
    return instability(k, dk, 0.0727, 997, h, dh, vpp, dvpp, 8.9e-4)


print(inst_water(4, 4, 5e-3, 210.5e-3))
