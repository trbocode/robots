import sys

"""
brownian() implements one dimensional Brownian motion (i.e. the Wiener process).
"""

# File: brownian.py

from math import sqrt
from scipy.stats import norm
import numpy as np


def brownian(x0, n, dt, delta,torus):
    """
    Generate an instance of Brownian motion (i.e. the Wiener process):

        X(t) = X(0) + N(0, delta**2 * t; 0, t)

    where N(a,b; t0, t1) is a normally distributed random variable with mean a and
    variance b.  The parameters t0 and t1 make explicit the statistical
    independence of N on different time intervals; that is, if [t0, t1) and
    [t2, t3) are disjoint intervals, then N(a, b; t0, t1) and N(a, b; t2, t3)
    are independent.
    
    Written as an iteration scheme,

        X(t + dt) = X(t) + N(0, delta**2 * dt; t, t+dt)


    If `x0` is an array (or array-like), each value in `x0` is treated as
    an initial condition, and the value returned is a numpy array with one
    more dimension than `x0`.

    Arguments
    ---------
    x0 : float or numpy array (or something that can be converted to a numpy array
         using numpy.asarray(x0)).
        The initial condition(s) (i.e. position(s)) of the Brownian motion.
    n : int
        The number of steps to take.
    dt : float
        The time step.
    delta : float
        delta determines the "speed" of the Brownian motion.  The random variable
        of the position at time t, X(t), has a normal distribution whose mean is
        the position at time t=0 and whose variance is delta**2*t.
    out : numpy array or None
        If `out` is not None, it specifies the array in which to put the
        result.  If `out` is None, a new numpy array is created and returned.

    Returns
    -------
    A numpy array of floats with shape `x0.shape + (n,)`.
    
    Note that the initial value `x0` is not included in the returned array.
    """

    x0 = np.asarray(x0)

    # For each element of x0, generate a sample of n numbers from a
    # normal distribution.
    r = norm.rvs(size=x0.shape + (n,), scale=delta*sqrt(dt))

    # This computes the Brownian motion by forming the cumulative sum of
    # the random samples. 
    #np.cumsum(r, axis=-1, out=out)
    r%=torus

    # Add the initial condition.
    r += np.expand_dims(x0, axis=-1)

    return r
for j in [1.5,2,3,4,5]:
    N=100000000
    torus=1
    t=0
    x=brownian(0, N, 1/1000000, 1,torus)
    x1=brownian(0, N, 1/1000000, 1,torus)
    y=brownian(0, N, 1/1000000, 1,torus)
    y1=brownian(0, N, 1/1000000, j,torus)
    grid=float(sys.argv[1])
    curr=[0,0]
    xs=0
    for i in range(N):
        if(((curr[0]%grid)<grid/2 and (curr[1]%grid)<grid/2) or ((curr[0]%grid)>=grid/2 and (curr[1]%grid)>=grid/2)):
            curr[0]+=y[i]
            curr[1]+=y1[i]
        else:
            curr[0]+=y[i]
            curr[1]+=x1[i]
            xs+=1
        curr[0]%=torus        
        curr[1]%=torus
    print(xs/(N-xs))
