import  random

def rand(left,right):
    return left+(right-left)*random.random()
 
def getpi():
    cnt = 0
    max = 100000
    x = 0.0
    y = 0.0

    for i in range(max):
        x = rand(-1.0,1.0)
        y = rand(-1.0,1.0)
        if x*x+y*y <= 1:
            cnt = cnt+ 1

    return cnt*4.0/max 
  

if __name__ == "__main__":

   for i in range(10):
       print getpi()

