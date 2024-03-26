import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

def load_session(session):
    file_path = "data" + str(session) + ".csv"
    data = np.loadtxt(file_path, delimiter=",")
    return data


def check_normal(session):
    data = load_session(session)
    length = len(data)
    p_value = stats.normaltest(data)
    print(f"p value is {p_value}")
    
    mean, std = stats.norm.fit(data)
    
    # Plot the histogram
    plt.hist(data, bins=30, density=True, alpha=0.6, color='g')
    
    # Plot the PDF (probability density function) of the fitted normal distribution
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mean, std)
    plt.plot(x, p, 'k', linewidth=2)
    
    plt.xlabel('Value')
    plt.ylabel('Probability')
    plt.title(f'Histogram of {length} Data with Fitted Normal Distribution')
    
    plt.show()
    return


def generate_data_points(session, chain_length):
    data = load_session(session)
    error = stats.sem(data)
    average = np.mean(data)
    return np.array([chain_length, average, error])


def show_data(session, x):
    length, avg, error = generate_data_points(session, x)
    print(f"Average is {avg}, error is {error}")


def power_law_offset(x, t0, c, delta):
    return c + t0 * np.power(x, delta)


def power_law(x, t0, delta):
    return t0 * np.power(x, delta)


def fitting(x, y, yerr, offset=False):
    length = len(x)
    if length != len(y) or length != len(yerr):
        print("Inputs have different dimensions!")
        return
    popt, pcov = curve_fit(power_law, x, y, sigma=yerr, absolute_sigma=True)
    t0_opt, delta_opt = popt
    t0_std_err, delta_std_err = np.sqrt(np.diag(pcov))

    y_pred = power_law(x, *popt)

    res = y - y_pred

    chi_squared = np.sum((res / yerr) ** 2)
    red_chi = chi_squared / (length - 2)

    print("\nOptimized parameters:")
    print(f"t0 = {t0_opt} +- {t0_std_err}")
    print(f"delta = {delta_opt} +- {delta_std_err}")
    print(f"Reduced Chi Squared is {red_chi}")
    xx = np.linspace(0, 100)
    plt.plot(xx, power_law(xx, t0_opt, delta_opt), label="Fit to power law")
    plt.errorbar(x, y, yerr=yerr, fmt='o', label='Data Points')

    plt.xlabel("Chain Length")
    plt.ylabel("Average Unknotting Time")
    plt.legend()
    plt.show()

    plt.figure()
    plt.errorbar(x, res, yerr=yerr, fmt='o')
    plt.axhline(0, color='black', linestyle='--')  # Add a horizontal line at y=0 for reference
    plt.xlabel('N - N0')
    plt.ylabel('Residuals')
    plt.grid(True)
    plt.show()

    if offset:
        popt2, pcov2 = curve_fit(power_law_offset, x, y, sigma=yerr, absolute_sigma=True)
        t0_opt2, c_opt2, delta_opt2 = popt2
        t0_std_err2, c_std_err2, delta_std_err2 = np.sqrt(np.diag(pcov2))

        print("Optimized parameters (with offset):")
        print(f"t0 = {t0_opt2} +- {t0_std_err2}")
        print(f"delta = {delta_opt2} +- {delta_std_err2}")
        print(f"offset = {c_opt2} +- {c_std_err2}")

        plt.plot(xx, power_law_offset(xx, t0_opt2, c_opt2, delta_opt2), label="Fit to power law (with offset)")


def results(info):
    arr = [generate_data_points(session, chain_length) for [session, chain_length] in info]
    x = [element[0] for element in arr]
    y = [element[1] for element in arr]
    yerr = [element[2] for element in arr]

    fitting(x, y, yerr)


def sinusoidal(x, a, b, c, d):
    return a * np.sin(b * x + c) + d


def frequency(info):
    arr = [generate_data_points(session, freq) for [session, freq] in info]
    x = np.array([element[0] for element in arr])
    y = np.array([element[1] for element in arr])
    yerr = np.array([element[2] for element in arr])

    popt, pcov = curve_fit(sinusoidal, x, y, sigma=yerr)
    a_fit, b_fit, c_fit, d_fit = popt
    perr = np.sqrt(np.diag(pcov))
    a_err = perr[0]
    b_err = perr[1]
    c_err = perr[2]
    d_err = perr[3]
    y_pred = sinusoidal(x, *popt)

    res = y - y_pred

    chi_squared = np.sum((res / yerr) ** 2)
    red_chi = chi_squared / (len(arr) - 4)

    plt.figure()
    plt.errorbar(x, y, yerr=yerr, fmt='o', label='Data Points')
    xx = np.linspace(11, 19)
    plt.plot(xx, sinusoidal(xx, a_fit, b_fit, c_fit, d_fit), label="Sinusoidal Fit")
    plt.ylim([0,40])
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Average Unknotting Time")

    print(f"Reduced chi squared is {red_chi}")
    print(f"a = {a_fit} +- {a_err}")
    print(f"b = {b_fit} +- {b_err}")
    print(f"c = {c_fit} +- {c_err}")
    print(f"d = {d_fit} +- {d_err}")

    plt.legend()
    plt.show()

    plt.figure()
    plt.errorbar(x, res, yerr=yerr, fmt='o')
    plt.axhline(0, color='black', linestyle='--')  # Add a horizontal line at y=0 for reference
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Residuals')
    plt.grid(True)
    plt.show()


part_1 = [[1, 78], [2, 10], [3, 50], [4,34]]
part_2 = [[9, 11], [6, 13], [4, 15], [7, 19], [8, 17], [10, 14], [11, 16], [12, 12]] # 5, 11 has wrong data

results(part_1)
# show_data(12, 12)
frequency(part_2)
