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
t=0.01



def CrossNorth(x,y,n):
    return ((x>=y) and (x<=(n-y)))
def CrossSouth(x,y,n):
    return ((x<=y) and (x>=(n-y)))
def CrossEast(x,y,n):
    return ((x>=y) and (x>=(n-y)))
def CrossWest(x,y,n):
    return ((x<=y) and (x<=(n-y)))
def GridSquare1(x,y,n):
    return (x<=n//2 and y<=n//2)
def GridSquare2(x,y,n):
    return (x>=n//2 and y<=n//2)
def GridSquare3(x,y,n):
    return (x<=n//2 and y>=n//2)
def GridSquare4(x,y,n):
    return (x>=n//2 and y>=n//2)
def SlopeBottom(x,y,n):
    return (x<y)
def SlopeTop(x,y,n):
    return (x>=y)
def WrapIn(x,y,n,m=2):
    return ((m*x-y)%n<n//2)
def CircInside(x,y,n,r=0.3):
    return ((x-n//2)**2+(y-n//2)**2)<(n*r)**2
def CircOutside(x,y,n,r=0.3):
    return not CircInside(x,y,r)
def false(*_):
    return False
def true(*_):
    return True
def ThroughX(x,y,n):
    return int(x)
def ThroughY(x,y,n):
    return int(y)

def l2norm(x1,y1,x2,y2):
    return (x1-x2)**2+(y1-y2)**2
def RobotSpeed(arr,range,close):
    speeds=np.ones(dim)
    for i in range(dim//2):
        for j in range(i+1,dim//2):
            if(l2norm(arr[2*i],arr[2*i+1],arr[2*j],arr[2*j+1])<range):
                speeds[i]==close
                speeds[j]==close
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


def MatGen2(func,n):
    ret=np.zeros((n**dim,n**dim))
    for i in range(n**dim):
        indicies=np.zeros(dim)
        tmp=i
        for j in range(dim):
            indicies[j]=tmp%n
            tmp=tmp//n
        for j in range(dim):
            if(j==0 and func(indicies[0],indicies[1],n)):
                if(func((indicies[0]-1)%n,indicies[1],n)):
                    ret[AddInd(indicies,j,-2,n)][i]+=1/4
                else:
                    ret[AddInd(indicies,j,-1,n)][i]+=1/4
                if(func((indicies[0]+1)%n,indicies[1],n)):
                    ret[AddInd(indicies,j,2,n)][i]+=1/4
                else:
                    ret[AddInd(indicies,j,1,n)][i]+=1/4
            elif(j==1 and func(indicies[0],indicies[1],n) and not func(indicies[0],indicies[1]+1,n)): #buttom row fast
                ret[AddInd(indicies,j,-1,n)][i]+=1/4
                ret[AddInd(indicies,j,1,n)][i]+=1/8
                indicies2=[(indicies[0]+1)%n,indicies[1]]
                ret[AddInd(indicies2,j,1,n)][i]+=1/8
            elif(j==1 and func(indicies[0],indicies[1],n) and not func(indicies[0],(indicies[1]-1)%n,n)): #top row fast
                ret[AddInd(indicies,j,1,n)][i]+=1/4
                ret[AddInd(indicies,j,-1,n)][i]+=1/8
                indicies2=[(indicies[0]+1)%n,indicies[1]]
                ret[AddInd(indicies2,j,-1,n)][i]+=1/8
            elif(j==1 and not func(indicies[0],indicies[1],n) and func(indicies[0],indicies[1]-1,n) and indicies[0]%2==1): #top row slow
                ret[AddInd(indicies,j,1,n)][i]+=1/4
                indicies2=[(indicies[0]-1)%n,indicies[1]]
                ret[AddInd(indicies2,j,-1,n)][i]+=1/4
            elif(j==1 and not func(indicies[0],indicies[1],n) and func(indicies[0],(indicies[1]+1)%n,n) and indicies[0]%2==1): #buttom row slow
                ret[AddInd(indicies,j,-1,n)][i]+=1/4
                indicies2=[(indicies[0]-1)%n,indicies[1]]
                ret[AddInd(indicies2,j,1,n)][i]+=1/4
            else:
                ret[AddInd(indicies,j,-1,n)][i]+=1/4
                ret[AddInd(indicies,j,1,n)][i]+=1/4
    return ret
def Graph(ei,n):
    for val in range(len(ei[0])):
        if np.allclose(1,ei[0][val]):
            ret=ei[1][:,val]
            ret=abs(ret)
            ret=ret/np.sum(ret)
            ret=ret.reshape((n,n))
            print(ret)
            plt.close('all')
            X= np.arange(0,1,1/n)
            Y= np.arange(0,1,1/n)
            X,Y=np.meshgrid(X,Y)
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            surf = ax.plot_surface(X, Y, ret, cmap=cm.cividis, linewidth=0.5,alpha=0.3, antialiased=False)
            plt.show()
            np.savetxt(sys.argv[1]+"ZvikaTry.txt",ret)
n=2*int(sys.argv[1])
mat=MatGen2(GridSquare1,n)
ei=np.linalg.eig(mat)
Graph(ei,n)
