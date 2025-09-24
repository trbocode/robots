import numpy as np
import math
from sklearn.preprocessing import normalize
from scipy.stats import norm
import sys
import random
import matplotlib.pyplot as plt
from matplotlib import cm
import tkinter 
import tkinter.filedialog 


ret=np.loadtxt("10ZvikaTry.txt")
n=ret.shape[0]
X= np.arange(0,1,1/n)
Y= np.arange(0,1,1/n)
plt.plot(ret[15],Y)
ret=np.loadtxt("20ZvikaTry.txt")
n=ret.shape[0]
X= np.arange(0,1,1/n)
Y= np.arange(0,1,1/n)
plt.plot(ret[30]*4,Y)
ret=np.loadtxt("30ZvikaTry.txt")
n=ret.shape[0]
X= np.arange(0,1,1/n)
Y= np.arange(0,1,1/n)
plt.plot(ret[45]*9,Y)
ret=np.loadtxt("40ZvikaTry.txt")
n=ret.shape[0]
X= np.arange(0,1,1/n)
Y= np.arange(0,1,1/n)
plt.plot(ret[60]*16,Y)
#X,Y=np.meshgrid(X,Y)
#fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#surf = ax.plot_surface(X, Y, ret, cmap=cm.cividis, linewidth=0.5,alpha=0.3, antialiased=False)
plt.show()
