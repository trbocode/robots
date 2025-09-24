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

dim=2
t=0.001


def l2norm(x1,y1,x2,y2):
    return (x1-x2)**2+(y1-y2)**2
def RobotSpeed(arr,ran,close,far):
    speeds=np.ones(dim)*far
    for i in range(dim//2):
        for j in range(i+1,dim//2):
            if(l2norm(arr[2*i],arr[2*i+1],arr[2*j],arr[2*j+1])<5):
                speeds[2*i]=close
                speeds[2*i+1]=close
                speeds[2*j]=close
                speeds[2*j+1]=close
    return speeds


def AddInd(Indicies,Ind,num,n):
    tmp=0
    for i in range(dim-1,-1,-1):
        tmp*=n
        if(i==Ind):
            tmp+=(Indicies[i]+num)%n
        else:
            tmp+=(Indicies[i])
    return(int(tmp))


def MatGen2(SpeedIn,SpeedOut,n):
    ret=np.zeros((n**dim,n**dim))
    for i in range(n**dim):
        indicies=np.zeros(dim)
        tmp=i
        for j in range(dim):
            indicies[j]=tmp%n
            tmp=tmp//n
        SpeedArr=np.square(RobotSpeed(indicies,1,SpeedIn,SpeedOut))
        for j in range(dim):
            #ret[AddInd(indicies,j,-1,n)][i]+=SpeedArr[j]**2/top*unloop
            #ret[AddInd(indicies,j,1,n)][i]+=SpeedArr[j]**2/top*unloop
            ret[AddInd(indicies,j,-1,n)][i]+=t/2*SpeedArr[j]
            ret[AddInd(indicies,j,1,n)][i]+=t/2*SpeedArr[j]
        ret[i][i]+=1-np.sum(SpeedArr)*t
    return ret
def Graph(ei,n,dim):
    for val in range(len(ei[0])):
        if np.allclose(1,ei[0][val]):
            ret=ei[1][:,val]
            ret=abs(ret)
            ret=ret/np.sum(ret)
            ret=ret.reshape([n]*dim)
            #plt.close('all')
            #X= np.arange(0,1,1/n)
            #Y= np.arange(0,1,1/n)
            #X,Y=np.meshgrid(X,Y)
            #fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            #surf = ax.plot_surface(X, Y, ret, cmap=cm.cividis, linewidth=0.5,alpha=0.3, antialiased=False)
            #plt.show()
            np.save("Dim"+str(dim)+"n"+str(n)+".txt",ret)

n=int(sys.argv[1])
dim=int(sys.argv[2])
SpeedIn=9
SpeedOut=1
mat=MatGen2(SpeedIn,SpeedOut,n)
ei=np.linalg.eig(mat)
Graph(ei,n,dim)
