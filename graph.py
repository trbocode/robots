import numpy as np

radius=3
invert=0 

def calc(array):
    flags=np.zeroes(len(array))
    for i in range(len(array)):
        for j in range(len(array)):
            if (i!=j && np.linalg.norm(array[i]-array[j])<radius):
                flags[i]=1
    short-num=np.sum(flags)
    return (len(array[0])*2)**(len(array)-short-num)*(len(array[0])*2+1)**short-num
