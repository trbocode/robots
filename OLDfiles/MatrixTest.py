import numpy as np
from sklearn.preprocessing import normalize

n=2
speed=2
eps=1

def GridSpeed(x,y,axis):
    if ((x<n//2) == (y<n//2)):
        if(axis==0):
            return 1/speed**2
        else:
            return 1
    else:
        if(axis==0):
            return 1
        else:
            return 1
def SpeedMatGen():
    mat0=np.zeros((n,n))
    mat1=np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            mat0[i][j]=GridSpeed(i,j,0)
            mat1[i][j]=GridSpeed(i,j,1)
    mat0=normalize(mat0,axis=0,norm='l1')
    mat1=normalize(mat1,axis=1,norm='l1')
    return mat0,mat1
def MatGen():
    ret=np.zeros((n**2,n**2))
    xax,yax=SpeedMatGen()
    for i in range(n**2):
        xco=i%n
        yco=i//n
        up=yax[xco,(yco-1)%n]
        left=xax[(xco-1)%n,yco]
        down=yax[xco,(yco+1)%n]
        right=xax[(xco+1)%n,yco]
        top=(up+left+right+down)
        ret[xco+((yco-1)%n)*n][xco+yco*n]+=up/top*eps
        ret[xco+((yco+1)%n)*n][xco+yco*n]+=down/top*eps
        ret[(xco-1)%n+yco*n][xco+yco*n]+=left/top*eps
        ret[(xco+1)%n+yco*n][xco+yco*n]+=right/top*eps
        ret[xco+yco*n][xco+yco*n]+=(1-eps)
    return ret

mat=MatGen()
print(np.transpose(mat))
ei=np.linalg.eig(np.transpose(mat))
print(ei)
for val in range(len(ei[0])):
    if np.allclose(1,ei[0][val]):
        print(ei[1][:,val].reshape((n,n)))


