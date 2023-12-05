"""
wenner_array_curve_finite_slab.py

    Wenner array master curve for a finite conductive slab bounded below by
        an infinitely resistive material.
    
    Key parameters to set are the width (W), length (L), and thickness (H)
        of the slab, and how finely each dimension is divided (N).

    Copyright (c) 2013-2016 University of Toronto
    Last Modification:  20 July 2016 by David Bailey
    Original Version:   22 March 2013 by Jason Mak 
    Contact: Jason Mak <jcc.mak@mail.utoronto.ca>

    License: Released under the MIT License; the full terms are this license
                are appended to the end of this file, and are also available
                at http://www.opensource.org/licenses/mit-license.php
"""

# Use python 3 consistent printing, unicode, and division
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division  # So dividing two integers gives a float

import numpy as np
from numpy import sqrt

import matplotlib.pyplot as plt
import time

start_time =time.time()

# parameters for the dimensions of the slab
W = 56.0e-2     # Width in metres
L = 96.5e-2     # Length in metres

H = 5e-2    # Height or depth in metres; for example; this will be normalized
N = 20      # need at least 10 to get accurate enough
            #       the time to run this program grows as N**3

a_normalized = np.linspace(0.001, 6, 50)  #same as the graph given as part of the experiment
a = a_normalized*H

# storing the values for the apparent resitiviity
rho_a_normalized = np.zeros_like(a)

# set locations of the array probes
# we assume that we will take the array on a line along the middle of the table
Vp_y = W/2.
Vn_y = W/2.
Ip_y = W/2.
In_y = W/2.

# method of images, calculating the effect of each mirrored charge
def geometric_factor_function(x, y, z,
                              I, J, K,
                              W, L, H,
                              dipole_coordinates,
                              geometrix_factor_max = 10.):

    #z_p, z_n always at 0
    x_p, y_p, x_n, y_n = dipole_coordinates

    r_p_sq = (x -((I+I%2)*L+(-1)**(I%2)*x_p))**2 +\
             (y -((J+J%2)*W+(-1)**(J%2)*y_p))**2 +\
             (z - (K*2.*H))**2
    r_p = sqrt(r_p_sq)

    r_n_sq = (x -((I+I%2)*L+(-1)**(I%2)*x_n))**2 +\
             (y -((J+J%2)*W+(-1)**(J%2)*y_n))**2 +\
             (z - (K*2.*H))**2
    r_n = sqrt(r_n_sq)
    
    result = (1/r_p - 1/r_n)

    if I+J+K == 0:
        result[result==np.inf] = geometrix_factor_max #set np.inf to 0
        result[result==-np.inf] = -geometrix_factor_max #set np.inf to 0
    return result

# summing the effects of each mirrored charge
def geometric_factor_array(array_x, array_y, array_z,
                           N,
                           W, L, H, dipole_coordinates):
    assert array_x.shape == array_y.shape
    assert array_x.shape == array_z.shape
    grid_shape = array_x.shape
    X_ravel = np.ravel(array_x)
    Y_ravel = np.ravel(array_y)
    Z_ravel = np.ravel(array_z)

    factor = np.zeros_like(X_ravel)
    alpha = [(i,j,k) for i in range(-N, N+1) for j in range(-N, N+1) \
             for k in range(-N, N+1)]
    for alpha_i in alpha:
        #saves memory
        factor += geometric_factor_function(X_ravel, Y_ravel, Z_ravel,
                                            alpha_i[0], alpha_i[1], alpha_i[2],
                                            W, L, H,
                                            dipole_coordinates)
    factor = factor.reshape(grid_shape)
    return factor

#iterate over the spacing of the Wenner array
for i, a_i in enumerate(a):
    #coordinates specific to wenner array
    Vp_x = L/2. - a_i/2.
    Vn_x = L/2. + a_i/2.
    Ip_x = L/2. - 3.*a_i/2.
    In_x = L/2. + 3.*a_i/2.

    V_x = np.array([Vp_x, Vn_x])
    V_y = np.array([Vp_y, Vn_y])
    V_z = np.zeros_like(V_x) 
    dipole_coordinates = (Ip_x, Ip_y, In_x, In_y)

    #calculate the 
    geometric_factor = geometric_factor_array(V_x, V_y, V_z,
                                              N,
                                              W, L, H,
                                              dipole_coordinates)

    #by substituting the formula for the method of images with the
    #apparent resistivity, we can obtain the following:
    mid_time = time.time()
    print("Iteration ",i, "out of ", len(a), " : ", 
                                    mid_time - start_time, 's')
    rho_a_normalized[i] = a_i*(geometric_factor[0] - geometric_factor[1])

#compare with data given in course website
##wennercurve = np.loadtxt('wennerk1.csv', delimiter = ',', skiprows = 1)

#some profiling
end_time = time.time()
print(end_time - start_time, 's')

np.savetxt('wenner_array_finite_slab.csv',
           np.column_stack([a_normalized, rho_a_normalized]),delimiter=',')


plt.title("Wenner Array Curve")
plt.grid(True, which='both')
plt.ylabel(r"normalized apparent resistivity [$\rho_a/\rho_0$]")
plt.xlabel("normalized spacing [$a/d$]")
measure_plt, = plt.plot(a_normalized, rho_a_normalized, 'o')
##theory_plt,= plt.plot(wennercurve[:,1], wennercurve[:,0], '-')

#asympotic behaviour
plt.plot(a_normalized, 2*np.log(2)*a_normalized, '--k')
plt.plot(a_normalized, np.ones_like(a_normalized), '--k')

label_string = "N = %d\n"%N +\
               "W = %0.3f \n"%(W) +\
               "L = %0.3f \n"%(L)

plt.text(0.25,0.75,
         label_string,
         horizontalalignment = 'left',
         verticalalignment = 'center',
         transform = plt.gca().transAxes)



##plt.legend([theory_plt, measure_plt],
##           ["Theory", "Measurement"])

plt.xlim(0,3)   #same as in the plot from the experiment handout
plt.ylim(0, 4.8)
plt.show()
"""

Full text of MIT License:

    Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""    
    
