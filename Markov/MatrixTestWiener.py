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
import itertools

dim=2
t=0.001



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


def AddInd(Indicies,n):
    tmp=0
    for i in range(dim-1,-1,-1):
        tmp*=n
        tmp+=Indicies[i]%n
    return int(tmp)


def MatGen2(SpeedsArr,func,func2,n):
    ret=np.zeros((n**dim,n**dim))
    SpeedsArr=np.square(SpeedsArr/np.max(SpeedsArr))
    for i in range(n**dim):
        indicies=np.zeros(dim)
        tmp=i
        for j in range(dim):
            indicies[j]=tmp%n
            tmp=tmp//n
        SpeedArr=SpeedsArr[int(func(indicies[0],indicies[1],n))][int(func2(indicies[0],indicies[1],n))]
        for arr in itertools.product(range(-1,2),repeat=dim):
            add=1
            for k in range(len(arr)):
                if(arr[k]==0):
                    add*=(1-SpeedArr[k])
                else:
                    add*=SpeedArr[k]/2
            ret[AddInd(indicies+arr,n)][i]=add
    return ret
def Graph(ei,n):
    for val in range(len(ei[0])):
        if np.allclose(1,ei[0][val]):
            ret=ei[1][:,val]
            ret=abs(ret)
            ret=ret/np.sum(ret)
            ret=ret.reshape((n,n))
            plt.close('all')
            X= np.arange(0,1,1/n)
            Y= np.arange(0,1,1/n)
            X,Y=np.meshgrid(X,Y)
            fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
            surf = ax.plot_surface(X, Y, ret, cmap=cm.cividis, linewidth=0.5,alpha=0.3, antialiased=False)
            plt.show()
            #np.savetxt("Epic.txt",ret)

def second(event):
    Kind=List1.curselection()
    if(Kind):
        List2.delete(0,'end')
        List3.delete(0,'end')
        for i in TypesDict[List1.get(Kind[0])]:
            List2.insert('end',i)
            List3.insert('end',i)
        List2.select_set('end')
        List3.select_set('end')
        List2.update_idletasks()
        List3.update_idletasks()
def parse():
        K1=List2.curselection()
        K2=List3.curselection()
        if(K1 and K2):
            func=FunctionsDict[List2.get(K1[0])]
            func2=FunctionsDict[List3.get(K2[0])]
        tup1=np.fromstring(Speed1X.get()+","+Speed1Y.get(),sep=',')
        tup2=np.fromstring(Speed2X.get()+","+Speed2Y.get(),sep=',')
        tup3=np.fromstring(Speed3X.get()+","+Speed3Y.get(),sep=',')
        SpeedsArr=[[tup3,tup2],[tup1,tup1]]
        n=int(Res.get())
        mat=MatGen2(SpeedsArr,func,func2,n)
        ei=np.linalg.eig(mat)
        Graph(ei,n)
def FileParse(entry):
    with open(entry) as fil:
        SpeedsArr=np.loadtxt(fil,dtype=np.float64,delimiter=",",skiprows=1)
    n=SpeedsArr.shape[0]
    print(n)
    SpeedsArr=np.reshape(SpeedsArr,(n,n,dim))
    mat=MatGen2(SpeedsArr,ThroughX,ThroughY,n)
    ei=np.linalg.eig(mat)
    Graph(ei,n)
def SetOpen():
    entry=tkinter.filedialog.askopenfilename()
    first.destroy()
    FileParse(entry)
TypesList=['Grid','Slope','Cross','Wrap','Circle']
TypesDict={'Grid':['Bottom Left','Bottom Right','Top Left','Top Right','Default'],'Slope':['Bottom','Top','Default'],'Cross':['East','South','West','North','Default'],'Wrap':['Inner','Default'],'Circle':['Inside','Outside','Default']}
FunctionsDict={'Bottom Left':GridSquare1,'Bottom Right':GridSquare2,'Top Left':GridSquare3,'Top Right':GridSquare4,'Default':false,'Bottom':SlopeBottom,'Top':SlopeTop,'East':CrossEast,'West':CrossWest,'North':CrossNorth,'South':CrossSouth,'Inner':WrapIn,'Inside':CircInside,'Outside':CircOutside}

if(len(sys.argv)<2):
    first=tkinter.Tk()
    tkinter.Label(first, text='Grid Type').grid(row=0)
    List1=tkinter.Listbox(first,height=len(TypesList),exportselection=False)
    for i in TypesList:
        List1.insert('end',i)
    List1.grid(row=0,column=1)
    List1.bind("<<ListboxSelect>>", second)
    tkinter.Label(first, text='Default: Speed X').grid(row=0,column=2)
    Speed3X=tkinter.Entry(first)
    Speed3X.grid(row=0,column=3)
    Speed3X.insert(0,"1")
    tkinter.Label(first, text='Speed Y').grid(row=0,column=4)
    Speed3Y=tkinter.Entry(first)
    Speed3Y.grid(row=0,column=5)
    Speed3Y.insert(0,"1")
    tkinter.Label(first, text='First Area').grid(row=1)
    List2=tkinter.Listbox(first,height=5,exportselection=False)
    List2.grid(row=1,column=1)
    tkinter.Label(first, text='Speed X').grid(row=1,column=2)
    Speed1X=tkinter.Entry(first)
    Speed1X.grid(row=1,column=3)
    Speed1X.insert(0,"1")
    tkinter.Label(first, text='Speed Y').grid(row=1,column=4)
    Speed1Y=tkinter.Entry(first)
    Speed1Y.grid(row=1,column=5)
    Speed1Y.insert(0,"1")
    tkinter.Label(first, text='Second Area').grid(row=2)
    List3=tkinter.Listbox(first,height=5,exportselection=False)
    List3.grid(row=2,column=1)
    tkinter.Label(first, text='Speed X').grid(row=2,column=2)
    Speed2X=tkinter.Entry(first)
    Speed2X.grid(row=2,column=3)
    Speed2X.insert(0,"1")
    tkinter.Label(first, text='Speed Y').grid(row=2,column=4)
    Speed2Y=tkinter.Entry(first)
    Speed2Y.grid(row=2 ,column=5)
    Speed2Y.insert(0,"1")
    tkinter.Label(first, text='Resolution').grid(row=3,column=0)
    Res=tkinter.Entry(first)
    Res.grid(row=3,column=1)
    Res.insert(0,"10")
    #tkinter.Label(first, text='FileName').grid(row=3,column=2)
    #Fname=tkinter.Entry(first)
    #Fname.grid(row=3,column=3)
    Ope=tkinter.Button(first,text='SettingsFile',command=SetOpen)
    Ope.grid(row=3,column=4)
    Start=tkinter.Button(first,text='Start',command=parse)
    Start.grid(row=4,column=3)
    Quit=tkinter.Button(first,text='Quit',command=first.destroy)
    Quit.grid(row=4,column=1)
    first.mainloop()


if(len(sys.argv)>1):
    FileParse(sys.argv[1])


