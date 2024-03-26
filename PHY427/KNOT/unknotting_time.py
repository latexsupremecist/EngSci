# -*- coding: utf-8 -*-
"""
unknotting_time.py
    Calculates the unknotting time and plots the knot survival
    distributions for a granular chain according to formulae from
    E. Ben-Naim, Z. A. Daya, P. Vorobieff, and R. E. Ecke,
    'Knots and Random Walks in Vibrated Granular Chains,'
    Phys. Rev. Lett 86 (2001) 1414-1417.

    Copyright (c) 2011-2015 University of Toronto
    Modifications:  5 April 2015 by David Bailey

    Original Version:   9 July 2011 by David Bailey
    Contact: David Bailey <dbailey@physics.utoronto.ca>
                            (http://www.physics.utoronto.ca/~dbailey)
    License: Released under the MIT License; the full terms are this license
                are appended to the end of this file, and are also available
                at http://www.opensource.org/licenses/mit-license.php
"""

# Use Python 3 compatible print and literals
from __future__ import print_function
from __future__ import unicode_literals

from   matplotlib import pyplot   # http://matplotlib.sourceforge.net/api/pyplot_api.html
import numpy             	# http://numpy.scipy.org/
from   numpy import exp, pi, sin, sqrt

""" All parameters are floats in SI units, unless otherwise specified. """

# Numerical Approximation parameters
#   define the largest loop range allowed,
#       i.e. for summing "infinite" series
quasiInfinity = 2**10
#   define the smallest step size,
#       i.e. for differentiation
epsilon = 1e-1

# Initial position of knot along chain
#   as a fraction of the total chain length.
#   i.e.  x=0.5 is the middle; 0 and 1 are the two ends
#   Note that the total chain length is N-N0, where N is the
#       actual number of beads in the chain, and N0
#       is the minimum number of beads in a knot, so
#       N-N0 is effective length of the chain in terms
#       of how far a crossing point can move.
#       This is fine for a single crossing point, but for
#       a knot with m crossing points, BenNaim's assumption
#       that N0 is equally shared among all m crossing points
#       is not obvious to me (DCB).
x0 = 0.5

# Number of crossing points in knot
#   m = 3 for a simple refoil knot
m = 3

# BenNaim Equation (4)
#   Probability that a single crossing point will survive a time t,
#   i.e. not have walked off the end of the chain
#   starting from fractional position along the chain x0
def s_t(t,x0):
    s_t = 0.0
    for k in range(quasiInfinity):
        s_t += (4.0/pi)*sin((2*k+1)*pi*x0)/(2*k+1)*exp(-((2*k+1)*pi)**2*t)
    return s_t

# BenNaim Equation (3)
#   Probability that m crossing points will all still survive after a time t,
#   all starting from fractional position along the chain x0
def S_m_t(m,t,x0):
    return numpy.power(s_t(t,x0),m)

# Calculate the numerical derivative of a function
#   using a second-order centered finite difference approximation.
#   WARNING: This will not work if the function or its derivative has a
#   discontinuity or singularity at (or near enough to) the point
#   being evaluated.
def derivative(f):
    # a good guess for the optimal finite difference step size
    #   is based on the machine epsilon given (approximately) by numpy
    root_eps = numpy.sqrt(numpy.finfo(float).eps)
    def df(x):
        # need to set minimum step size to avoid zero divides
        h = root_eps*numpy.maximum(1,x)
        return ( f(x+h) - f(x-h) ) / (2*h)
    return df

# Exit time probability function:R_m_t = - dS_m_t/dt
def R_m_t(m,t,x0):
    def S(t):
        return -S_m_t(m,t,x0)
    return derivative(S)

# generate linearly spaced times for plotting and calculation,
#   avoiding the discontinuity at t=0.
t = numpy.linspace(0.00001,0.7,500)
S = S_m_t(m,t,x0) # Evaluate S at the selected times t
R = R_m_t(m,t,x0)(t)

# Calculate the average unknotting time and standard deviation
#   From Ben-Naim, tau = 1/8, 0.073671, 0.056213 for m = 1,2,3 respectively
tau = numpy.average(t,weights=R)
std = sqrt(numpy.dot(R, (t-tau)**2)/R.sum())/tau
peak = t[R.argmax()]/tau
print("Number of crossings in knot        = ", m)
print()
print("Average unknotting time            = ", tau)
print("Standard Deviation / Average       = ", std)
print("Most Probable Decay Time / Average = ", peak)
print()
print("Note: The average unknotting time is given in units of D/(N-N0)**2")
print("      Where N  = number of beads in the chain,")
print("            N0 = number of beads in the knot, and")
print("            D  = hopping rate, i.e. steps per second.")

# Plot

fig = pyplot.figure(figsize=(8, 7)) # initialize figure

# subplot(211) means two rows; one column, plot number one,
S_vs_t = fig.add_subplot(211)
S_vs_t.plot(t/tau,S)
pyplot.ylabel("S(t)                 \n Fraction surviving")
# S_vs_t.set_yscale('log') # set logarithmic y axis, if desired
R_vs_t = fig.add_subplot(212)
R_vs_t.plot(t/tau,R)
# R_vs_t.set_yscale('log') # set logarithmic y axis, if desired
pyplot.ylabel("R(t)                    \n Unknotting probability")
pyplot.xlabel("t \n (unknotting time / average)", horizontalalignment='center')

pyplot.show()   # show the plots

# End of unknotting_time.py

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
