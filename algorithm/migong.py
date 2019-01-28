'''
    Recursive algorithm to slove maze.
    The init maze is 6*6 array, The vale 0 is block, the value 1 is pass   
    the func of walk() is a recursive function.

'''
maze=[
      [1,0,1,1,1,1],
      [1,1,1,0,0,1],
      [0,1,0,0,0,1],
      [1,1,0,1,0,1],
      [0,1,1,1,0,1],
      [1,1,0,1,1,1]]

SUCCESS = 0
         
def valid(maze, x, y):
    
    if(x >= 0 and x < len(maze) and y >= 0 and  y < len(maze)):
        if maze[x][y] == 1:
            return True
    return False

def walk(maze, x, y):
    global SUCCESS

    if(x == 0 and y == 0):
        maze[x][y]=2
        print("successful!")
        SUCCESS = 1 
        return True
    
    if SUCCESS !=1 and valid(maze,x,y) :
        maze[x][y] =2
        print(x,y)
        walk(maze, x-1, y)
        walk(maze, x, y-1)
        walk(maze, x+1, y)
        walk(maze, x, y+1)  

    else:
        return False


for i in range (6):
    print(maze[i])

walk(maze,3,3)

for i in range (6):
    print(maze[i])

