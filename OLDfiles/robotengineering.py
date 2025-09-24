import random
import numpy as np
import math
#import itertools
import sys

np.set_printoptions(linewidth=999)

def normwrap(vec1,vec2,innerfunc,outerfunc):
    sum=0
    for i in range(dim):
        sum+=innerfunc(vec1[i],vec2[i])
    return outerfunc(sum)

def l1norm(vec1,vec2):
    return normwrap(vec1,vec2,lambda vec1,vec2: min(abs(vec1-vec2),torus-abs(vec1-vec2)), lambda x:x)
def l2norm(vec1,vec2):
    return normwrap(vec1,vec2,lambda vec1,vec2: min(abs(vec1-vec2),torus-abs(vec1-vec2))**2, math.sqrt)


def linfnorm(vec1,vec2):
    maxi=0
    for i in range(dim):
        diff=min(abs(vec1[i]-vec2[i]),torus-abs(vec1[i]-vec2[i]))
        if(diff>max):
            maxi=diff
    return maxi

def simulation(robots=30,dim=2,torus=11,r=1,speedclose=0.2,speedfar=20,minrobot=1,iterations=9999,progress=1):
    robotarr=torus*np.random.random_sample((robots,dim))
    for k in range(iterations):
        detected={}
        deti=np.zeros(robots)
        for i in range(robots):
            #tup=tuple((j-j%r) for j in robotarr[i])
            tup=(robotarr[i][0]-robotarr[i][0]%r,robotarr[i][1]-robotarr[i][1]%r)
            if tup not in detected:
                detected[tup]=[]
            detected[tup].append(i)
        for i in range(robots):
            #tup=tuple((j-j%r) for j in robotarr[i])
            tup=(robotarr[i][0]-robotarr[i][0]%r,robotarr[i][1]-robotarr[i][1]%r)
            #for j in itertools.product(range(-1,2),repeat=dim):
            for j in range(-1,2):
                for l in range(-1,2):
                    #new=tuple((tup[i]+j[i]*r)%torus for i in range(dim))
                    new=((tup[0]+j*r)%torus,(tup[1]+l*r)%torus)
                    if (new in detected):
                        for  rob in detected[new]:
                            if i!=rob and (l2norm(robotarr[i],robotarr[rob])<r):
                                deti[i]+=1
                            if (deti[i]>=minrobot):
                                break
                        if (deti[i]>=minrobot):
                            break
                if (deti[i]>=minrobot):
                            break
        for i in range(robots):
            speed=speedfar
            if(deti[i]>=minrobot):
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
    if len(sys.argv)==11:
            robots=int(sys.argv[1]) # in paper, N=30
            dim=int(sys.argv[2])
            torus=int(sys.argv[3]) # L/n^1/dim=2, so L=2*n^1/dim
            r=float(sys.argv[4])
            speedclose=float(sys.argv[5]) # Vi, 
            speedfar=float(sys.argv[6]) # Vo
            minrobot=float(sys.argv[7]) # Vo
            iterations=int(sys.argv[8])
            times=int(sys.argv[9])
            progress=int(sys.argv[10])
            random.seed()
            resultarr=np.zeros([times,robots-1])
            savearr=np.zeros([times,robots,dim])
            for i in range(times):
                if (dim==2):
                    robotarr=simulation(robots,dim,torus,r,speedclose,speedfar,minrobot,iterations,progress)
                for j in range(robots-1):
                    resultarr[i][j]=l2norm(robotarr[0],robotarr[j+1])
                    for k in range(dim):
                        savearr[i][j][k]=robotarr[j][k]
                savearr[i][j]=robotarr[robots-1]
                print("run number"+str(i))
            savearr.tofile(str(speedclose)+"save.txt")
            resultarr.sort()
            resultarr2=np.zeros([times,20])
            for i in range(times):
                for j in range(robots-1):
                    resultarr2[i][int((resultarr[i][j])//(torus/20))]+=1
            print(resultarr2)
            np.savetxt(str(speedclose)+"out.csv", resultarr2, fmt='%d', delimiter="	")
    else:
        print("Arguments:")
        print ("1 - Amount of robots, 30 in paper")
        print ("2 - Dimention of space, 2 default")
        print ("3 - Size of space, as of n*bots^1/dim*")
        print ("4 - Radius of activation for bots, default 1")
        print ("5 - Speed when bots are close, default 0.2")
        print ("6 - Speed when robots are far, Default 20")
        print ("7 - Min num of robots to change speed, Default 1")
        print ("8 - Number of iterations (Default 9999)")
        print ("9 - Number of loops (Default 1)")
        print ("10 - If to show progress")
        print(" Example - python robotengineering.py 30 2 2 1 0.2 20 1 9999 2 1")

