'''
    Recursive algorithm to slove maze.
    The init maze is 6*6 array, The vale 0 is block, the value 1 is pass   
    the func of walk() is a recursive function.

'''
import copy
maze_1=[
      [1,0,1,1,1,1],
      [1,1,1,0,0,1],
      [0,1,0,0,0,1],
      [1,1,0,1,0,1],
      [0,1,1,1,0,1],
      [1,1,0,1,1,1]]


class Maze(object):
   
    def __init__(self, **kwargs):

        self.maze = kwargs['maze']
        self.success = 0
        self.end_x   = kwargs['end_x']
        self.end_y   = kwargs['end_y']

    
    def _valid(self,x,y):
        ''' x ,y in the range of maze, and the value of maze[x][y] is 1 '''
 
        if(x >= 0 and x < len(self.maze) and y >= 0 and  y < len(self.maze)):
            if self.maze[x][y] == 1:
                return True
        return False 
    
    def walk(self,x,y):

        if(x == self.end_x and y == self.end_y):
            self.maze[x][y]=2
            print("successful!")
            self.success = 1 
            return True
    
        if self.success !=1 and self._valid(x,y) :
            self.maze[x][y] = 2
            if ((self.walk( x-1, y)) or
                (self.walk( x, y-1)) or
                (self.walk( x+1, y)) or
                (self.walk( x, y+1))) : 
                
                return True  
            else:
                self.maze[x][y] = 1

        return False



if __name__ == "__main__":
    kwargs={}
    kwargs['maze'] = copy.deepcopy(maze_1)
    kwargs['end_x']= 5
    kwargs['end_y'] =5
    my_maze = Maze( **kwargs)
    for i in range (len(my_maze.maze)):
         print(my_maze.maze[i])
    my_maze.walk(0,0)       
    for i in range (len(my_maze.maze)):
         print(my_maze.maze[i])

