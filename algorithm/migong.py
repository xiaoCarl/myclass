'''
    Recursive algorithm to slove maze.
    The init maze is 6*6 array, The vale 0 is block, the value 1 is pass   
    the func of walk() is a recursive function.

'''
from __future__ import print_function
import copy
import time
import os

maze_1=[
      [1,0,1,1,1,1,0,1,1,1],
      [1,1,0,0,0,1,0,1,0,1],
      [0,1,0,0,1,1,1,1,0,1],
      [1,1,0,1,1,0,0,1,1,1],
      [1,0,0,1,1,1,1,1,1,0],
      [1,0,0,1,0,1,0,0,0,0],
      [1,1,0,1,0,1,0,1,1,1],
      [0,1,0,1,0,1,0,1,0,1],
      [0,1,1,1,0,1,0,1,0,1],
      [1,1,0,1,0,1,1,1,0,1]]


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
            self.success = 1
            self.graphic(x,y) 
            return True
    
        if self._valid(x,y):
            self.graphic(x,y)
        else:
            return False

        if self.success !=1  :
            self.maze[x][y] = 2
            if ((self.walk( x-1, y)) or
                (self.walk( x, y-1)) or
                (self.walk( x+1, y)) or
                (self.walk( x, y+1))) : 
                
                return True  
            else:
                self.maze[x][y] = 1

        return False

    def graphic(self,x,y):
        width  = len(self.maze)
        height = len(self.maze)
        
        time.sleep(1)
        os.system('clear')

        print("Start Location: 0 0") 
        print("End Location: ",self.end_x,self.end_y)
        print("Current Loction:",x,y)
        print()

        for x in range(width):
            print("{0:8}".format(x), end='' )
        print('\r\n')
      
        for i in range(height - 1, -1, -1):
            print("{0:4d}".format(i), end='')

            for j in range(width):
                p = self.maze[i][j]
                if p == 1:
                    print('_'.center(8), end='')
                elif p == 2:
                    print('O'.center(8), end='')
                else:
                    print('X'.center(8), end='')
            print('\r\n\r\n')


if __name__ == "__main__":

    kwargs = {}
    kwargs['maze']  = copy.deepcopy(maze_1)
    kwargs['end_x'] = 9
    kwargs['end_y'] = 9
    
    my_maze = Maze(**kwargs)    
    my_maze.walk(0,0)
       
