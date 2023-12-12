import numpy as np
import matplotlib.pyplot as plt

data_file = "data.txt"
sample_x = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.38448, 2.15963, 2.83217, 3.60828, 4.40192, 5.12361, 5.94211])
sample_y = np.array([1, 1, 1.01844, 1.03723, 1.09568, 1.15742, 1.22265, 1.30103, 1.3997, 1.50584, 2, 3, 4, 5, 6, 7, 8])

d = 0.05
rho = 1e-4

x_sigma_set, y_sigma_set = None, None
#  Linear systematics
x_offset, dx_offset, x_scale, dx_scale = None, None, None, None
y_offset, dy_offset, y_scale, dy_scale = None, None, None, None

try : # Default delimiter is whitespace
    Data = np.loadtxt( data_file, comments='#', unpack = True)
except : # But comma delimiters are also okay
    Data = np.loadtxt( data_file, comments='#', unpack = True, delimiter=',')
# Default format is for each data point line to have 4 values in this
#         order: x value, x uncertainty, y value, y uncertainty
if len(Data) == 4 :  # Default format
    x_in_file, x_sigma_in_file, y_in_file, y_sigma_in_file = Data
    # A scale factor is occasionally useful for handling systematics of
    #   measurements taken on different ranges of an instrument, but if
    #   not given it can be assumed to be 1.
    scale_factor      = np.array([1]*len(x_in_file))
elif   len(Data) == 5 :
    # If data points do have a scale factor, it is the 5th value.
    x_in_file, x_sigma_in_file, y_in_file, y_sigma_in_file, \
                scale_factor = Data
else :
    print("WARNING!!! Input data file has illegal number of columns!")

# Check if there are any offset or scale systematic uncertainties
#     assuming x_true = a_x + b_x * x_measured
#     assuming y_true = a_y + b_y * y_measured
sys_x, sys_y = [0, 0, 1, 0], [0, 0, 1, 0]
with open(data_file) as file:
    for i,line in enumerate(file):
        if   line.startswith('#  a_x, da_x, b_x, db_x =') :
            sys_x = [float(f) for f 
                         in line.rstrip().split("=")[1].split(",")]
        elif line.startswith('#  a_y, da_y, b_y, db_y =') :
            sys_y = [float(f) for f 
                         in line.rstrip().split("=")[1].split(",")]

# Set systematic uncertainties that have not been previously defined
#    Offset and offset uncertainty are multiplied by the scale factor.
            
if x_offset  == None : x_offset  = sys_x[0]*scale_factor
if dx_offset == None : dx_offset = sys_x[1]*scale_factor
if x_scale   == None : x_scale   = sys_x[2]
if dx_scale  == None : dx_scale  = sys_x[3]
if y_offset  == None : y_offset  = sys_y[0]*scale_factor
if dy_offset == None : dy_offset = sys_y[1]*scale_factor
if y_scale   == None : y_scale   = sys_y[2]
if dy_scale  == None : dy_scale  = sys_y[3]

# Applied systematic scaling to data
x_data  = ( x_offset + x_in_file * x_scale ) * scale_factor
y_data  = ( y_offset + y_in_file * y_scale ) * scale_factor
# Set random uncertainties from file if they are 
#           not set in the code above
if x_sigma_set == None :
    x_sigma = x_sigma_in_file * x_scale
else :
    x_sigma = x_sigma_set * x_scale
if y_sigma_set == None :
    y_sigma = y_sigma_in_file * y_scale
else :
    y_sigma = y_sigma_set * y_scale

plt.plot(sample_x, sample_y, color="g")
plt.plot(x_data/d, y_data/rho, color="b")
plt.show()
