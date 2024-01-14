import numpy as np

k=7
r=2
dim=1
radius=4

def parsesingle(ind):
    ret=np.zeros(dim)
    for i in range(dim):
        ret[i]=ind%k
        ind=ind/k
    return ret



def parsepos(ind):
    ret=np.zeros([r,dim])
    for i in range(r):
        
        ret[i]=parsesingle(ind%(k**dim))
        ind=ind/(k**dim)
    return ret

def botcheck(bot,botafter):
    flag=False
    for i in range(dim):
        if (bot[i]==botafter[i]+1 or bot[i]+1==botafter[i] or bot[i]==botafter[i]+k-1 or bot[i]+k-1==botafter[i]):
            if (flag):
                return False
            flag=True
    return flag

def l1norm(vec1,vec2):
    sum=0
    for i in range(dim):
        sum+=min(abs(vec1[i]-vec2[i]),abs((k-vec1[i])-vec2[i]))
    return sum


def check(pos,posafter):
    flags=np.zeros(r)
    for i in range(r):
        for j in range(r):
            if (i!=j and l1norm(pos[i],pos[j])<radius): #change < for >= if using other type of robot
                flags[i]=1
    flag=1
    for i in range(r):
        if (flags[i]==1 and pos[i]==pos[j]):
            continue
        if(not botcheck(pos[i],posafter[i])):
            flag=0
    return flag



mat=np.zeros([k**(dim*r),k**(dim*r)])
for i in range(np.shape(mat)[0]):
    for j in range(np.shape(mat)[1]):
        pos=parsepos(i)
        posafter=parsepos(j)
        mat[i][j]=check(pos,posafter)
         
