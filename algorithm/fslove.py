import math
import numpy as np

from  scipy.optimize import fsolve



def f03(x):
    y = [0,0,0]
    y[0] = 3.0*x[0]-math.cos(x[1])*x[2]-0.5 
    y[1] = x[0]**2-81*(x[1]+0.1)**2+math.sin(x[2])+1.06
    y[2] = math.e**(-x[0]*x[1])+20.0*x[2]+(10.0*math.pi-3)/3.0
    return y

r = fsolve(f03,[0.1,0.1,-0.1])
print(r)


def f04():
    x = [0.1,0.1,-0.1]
    x1= [0,0,0]

    delta =(x1[0]-x[0])**2+(x1[1]-x[1])**2+(x1[2]-x[2])**2
    print(delta)
    while delta >= 0.000001:
        print(delta) 
        x1[0] = 1.0/3*math.cos(x[1])*x[2]+1.0/6
        x1[1] = 1.0/9*math.sqrt(x[0]**2+math.sin(x[2])+1.06)-0.1
        x1[2] = -1.0/20*math.e**(-x[0]*x[1])-(10.0*math.pi-3)/60.0       
        
        delta =(x1[0]-x[0])**2+(x1[1]-x[1])**2+(x1[2]-x[2])**2
        x = x1

    return x1


print(f04())




