import numpy as np
from scipy.stats import norm
import math


np.set_printoptions(linewidth=999)

def normwrap(vec1,vec2,innerfunc,outerfunc):
    sum=0
    for i in range(len(vec1)):
        sum+=innerfunc(vec1[i],vec2[i])
    return outerfunc(sum)

def l1norm(vec1,vec2):
    return normwrap(vec1,vec2,lambda vec1,vec2: min(abs(vec1-vec2),torus-abs(vec1-vec2)), lambda x:x)
def l2norm(vec1,vec2):
    return normwrap(vec1,vec2,lambda vec1,vec2: min(abs(vec1-vec2),torus-abs(vec1-vec2))**2, math.sqrt)


def linfnorm(vec1,vec2):
    maxi=0
    for i in range(len(vec1)):
        diff=min(abs(vec1[i]-vec2[i]),torus-abs(vec1[i]-vec2[i]))
        if(diff>max):
            maxi=diff
    return maxi

def brownian(x0, n, dt, delta, torus, out=None):
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

    r = norm.rvs(size=x0.shape + (n,), scale=delta*math.sqrt(dt))

    # If `out` was not given, create an output array.
    if out is None:
        out = np.empty(r.shape)

    # This computes the Brownian motion by forming the cumulative sum of
    # the random samples. 
    np.cumsum(r, axis=-1, out=out)

    # Add the initial condition.
    out += np.expand_dims(x0, axis=-1)

    out %= torus

    return out






# The Wiener process parameter.
delta = 5
# Total time.
T = 100000000.0
# Number of steps.
N = 500000
# Time step size
dt = T/N
# Number of processes
count = 4
# Torus size
torus = 3000
# Radius of activation
rad = 500
# How much interior is slower - i.e vo/vi
speed = 0.2
# Initial values of x.
x = np.empty((count,2,N+1))
for i in range(count):
    #x[i,:, 0] = np.random.uniform(0,torus)
    x[i,:, 0] = 0.0
    brownian(x[i,:,0], N, dt, delta, torus, out=x[i,:,1:])


res=np.zeros(count*(count-1)//2)
l=-1 
for i in range(count):
    for j in range(i+1,count):
        l+=1
        for k in range(N+1): 
            if (l2norm(x[i,:,k],x[j,:,k])<rad):
                res[l]+=1
expected=rad**2*np.pi/(torus**2)
for i in range(len(res)):
    res[i]=(res[i]*speed)/(res[i]*speed+(N+1-res[i]))
print(res)
print(np.average(res))
print(expected*speed/(expected*speed+1-expected))
