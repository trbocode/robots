import numpy as np
from scipy.stats import norm
import math
import multiprocessing
import itertools

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


def simulation(arr):
    time=np.zeros(2,dtype=int)
    ret=np.zeros(6)
    while (max(time)<N):
        ret[3]+=1
        check=np.zeros(3)
        yes=0
        if (l2norm(x[arr[0],:,time[0]],x[arr[1],:,time[1]])<rad):
            check[0]=1
            check[1]=1
            yes+=1
        for u in range(2):
            if(check[u]==1):
                    ret[u]+=speedin
                    time[u]+=speedin
            else:
                    time[u]+=speedout
        ret[5-yes]+=1
    return ret




# The Wiener process parameter.
delta = 5
# Total time.
T = 100000000.0
# Number of steps.
N = 5000000
# Time step size
dt = T/N
# Number of processes
count = 8
# Torus size
torus = 5
# Radius of activation
rad = 1
# How much interior is slower - i.e vo/vi
speedin = 100
speedout = 1
speed=speedout/speedin
# Initial values of x.
x = np.empty((count,2,N+1))
for i in range(count):
    #x[i,:, 0] = np.random.uniform(0,torus)
    x[i,:, 0] = 0.0
    brownian(x[i,:,0], N, dt, delta, torus, out=x[i,:,1:])


res=np.zeros((count*(count-1))//2)
l=-1
with multiprocessing.Pool(20) as p:
    ret1=p.map(simulation,itertools.combinations(range(count),2))
ret1=sum(ret1)
piapprox=ret1[4]
totime=ret1[3]
print(piapprox/totime*(torus**2))
print(ret1[5]/totime*(torus**2))
print(totime)

