import numpy as np
from sklearn.preprocessing import normalize
from scipy.stats import norm
import sys
import random
import matplotlib.pyplot as plt
from matplotlib import cm
n=50
speed=2
dim=2
name="Yes.txt"


def CheckSpeed(arr,condition,condition2):
    if (condition(arr[0],arr[1])):
        return tup1
    elif(condition2(arr[0],arr[1])):
        return tup2
    else:
        return tup3


def crossnorth(x,y):
    return ((x>=y) and (x<=(n-y)))
def crosssouth(x,y):
    return ((x<=y) and (x>=(n-y)))
def crosseast(x,y):
    return ((x>=y) and (x>=(n-y)))
def crosswest(x,y):
    return ((x<=y) and (x<=(n-y)))
def crossdefault(x,y):
    return False
def griddefault(x,y):
    return False
def gridsquare1(x,y):
    return (x<=n//2 and y<=n//2)
def gridsquare2(x,y):
    return (x>=n//2 and y<=n//2)
def gridsquare3(x,y):
    return (x<=n//2 and y>=n//2)
def gridsquare4(x,y):
    return (x>=n//2 and y>=n//2)
def slopebottom(x,y):
    return (x<y)
def slopetop(x,y):
    return (x>=y)
def slopedefault(x,y):
    return False
def wrapdefault(x,y):
    return False
def wrapin(x,y,m=2):
    return ((m*x-y)%n<n//2)
def circinside(x,y,r=0.3):
    return ((x-n//2)**2+(y-n//2)**2)<(n*r)**2
def circoutside(x,y,r=0.3):
    return not CircInside(x,y,r)
def circdefault(x,y,r):
    return False
def false(*_):
    return False
def true(*_):
    return True

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


def AddInd(Indicies,Ind,num):
    tmp=0
    for i in range(dim-1,-1,-1):
        tmp*=n
        if(i==Ind):
            tmp+=(Indicies[i]+num)%n
        else:
            tmp+=(Indicies[i])
    return(int(tmp))

func=gridsquare1
func2=gridsquare4
tup1=(speed**2,1)
tup2=(1,speed**2)
tup3=(1,1)


def MatGen2():
    ret=np.zeros((n**dim,n**dim))
    tr=CheckSpeed([0]*dim,true,false)
    fl=CheckSpeed([0]*dim,false,false)
    fl2=CheckSpeed([0]*dim,false,true)
    supsum=np.sum(tr)+np.sum(fl)+np.sum(fl2)
    for i in range(n**dim):
        indicies=np.zeros(dim)
        tmp=i
        for j in range(dim):
            indicies[j]=tmp%n
            tmp=tmp//n
        SpeedArr=CheckSpeed(indicies,func,func2)
        unloop=np.sum(SpeedArr)/supsum
        top=2*np.sum(SpeedArr)
        #loop=
        for j in range(dim):
            ret[AddInd(indicies,j,-1)][i]+=SpeedArr[j]/top*unloop
            ret[AddInd(indicies,j,1)][i]+=SpeedArr[j]/top*unloop
        ret[i][i]+=(1-unloop)
    return ret


if(len(sys.argv)>1):
    with open(sys.argv[1]) as fil:
        lines1=fil.read().splitlines()
        lines=[i.split(" ") for i in lines1]
        func=getattr(sys.modules[__name__],(lines[0][0]+lines[1][0]).lower())
        func2=getattr(sys.modules[__name__],(lines[0][0]+lines[2][0]).lower())
        tup1=np.fromstring(lines[1][1],sep=',')
        tup2=np.fromstring(lines[2][1],sep=',')
        tup3=np.fromstring(lines[3][1],sep=',')
        n=int(lines[4][1])
        name=lines1[0]+" "+lines1[1]+" "+lines1[2]+" "+lines1[3]+" "+lines1[4]+".txt"
    if(len(sys.argv)>2):
        name=sys.argv[2]
mat=MatGen2()
#print(np.transpose(mat))
ei=np.linalg.eig(mat)
for val in range(len(ei[0])):
    if np.allclose(1,ei[0][val]):
        ret=ei[1][:,val].reshape((n,n))
        ret=abs(ret)
        X= np.arange(0,1,1/n)
        Y= np.arange(0,1,1/n)
        X,Y=np.meshgrid(X,Y)
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(X, Y, ret, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.show()
        np.savetxt(name,ret)


