import random
import numpy as np
import math
import sys

def normwrap(vec1,vec2,innerfunc,outerfunc):
    sum=0
    for i in range(dim):
        sum+=innerfunc(vec1[i],vec2[i])
    return outerfunc(sum)

def l1norm(vec1,vec2):
    return normwrap(vec1,vec2,lambda vec1,vec2: min(abs(vec1-vec2),abs((torus-vec1)-vec2)), lambda x:x)
def l2norm(vec1,vec2):
    return normwrap(vec1,vec2,lambda vec1,vec2: min(abs(vec1-vec2),abs((torus-vec1)-vec2))**2, math.sqrt)


def linfnorm(vec1,vec2):
    maxi=0
    for i in range(dim):
        diff=min(abs(vec1[i]-vec2[i]),abs((torus-vec1[i])-vec2[i]))
        if(diff>max):
            maxi=diff
    return maxi


def simulation(robots=30,dim=2,torus=11,r=1,speedclose=0.2,speedfar=20,iterations=9999,progress=1):
    robotarr=torus*np.random.random_sample((robots,dim))
    for k in range(iterations):
        detected=np.zeros(robots)
        for i in range(robots):
            if (not detected[i]):
                for j in range(robots):
                    if i!=j and (l1norm(robotarr[i],robotarr[j])<r):
                        detected[i]=1
                        detected[j]=1
                        break
            speed=speedfar
            if(detected[i]):
                speed=speedclose
            angleold=1
            for j in range(dim-1):
                angle=random.random()*math.pi
                robotarr[i][j]+=speed*math.sin(angle)*angleold
                robotarr[i][j]%=torus
                angleold*=math.cos(angle)
            robotarr[i][dim-1]+=speed*angleold
            robotarr[i][dim-1]%=torus
        if(progress and k%(iterations//20)==0):
            print("{:.0f}".format(100*k/iterations) + "%")
    return robotarr



if __name__=="__main__":
    if len(sys.argv)==10:
            robots=int(sys.argv[1]) # in paper, N=30
            dim=int(sys.argv[2])
            torus=int(sys.argv[3])*robots**(1/dim) # L/n^1/dim=2, so L=2*n^1/dim
            r=float(sys.argv[4])
            speedclose=float(sys.argv[5]) # Vi, 
            speedfar=float(sys.argv[6]) # Vo
            iterations=int(sys.argv[7])
            times=int(sys.argv[8])
            progress=int(sys.argv[9])
            random.seed()
            resultarr=np.zeros([times,robots-1])
            for i in range(times):
                robotarr=simulation(robots,dim,torus,r,speedclose,speedfar,iterations,progress)
                for j in range(robots-1):
                    resultarr[i][j]=l2norm(robotarr[0],robotarr[j+1])
            print(resultarr)
    else:
        print("Arguments:")
        print ("1 - Amount of robots, 30 in paper")
        print ("2 - Dimention of space, 2 default")
        print ("3 - Size of space, as of n*bots^1/dim*")
        print ("4 - Radius of activation for bots, default 1")
        print ("5 - Speed when bots are close, default 0.2")
        print ("6 - Speed when robots are far, Default 20")
        print ("7 - Number of iterations (Default 9999)")
        print ("8 - Number of loops (Default 1)")
        print ("9 - If to show progress")
        print(" Example - python robotengineering.py 30 2 2 1 0.2 20 9999 2 1")

