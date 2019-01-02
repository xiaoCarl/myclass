# -*- coding: UTF-8 -*-

'''
m:表示传球次数
n:表示第n个人
dfs(m,n): 第n个人传球m次后，仍然在第n个人手里次数f[m][n]
f[m][n]=dfs(m-1,n+1)+dfs(m-1,n-1)
used[m][n]=1:表示该值count[m][n]已经计算过，不需要再计算
'''

import numpy as np
used  = np.zeros((40,40),dtype=np.int32)
f = np.zeros((40,40),dtype=np.int32)
N = 0
M = 0

def dfs(m,n):
    if m < 0 : return 0
    if used[m][n] == 0:
        f[m][n] = dfs(m-1,(n-1+N)%N)+dfs(m-1,(n+1)%N)
    used[m][n] = 1
    return f[m][n]

if __name__ == '__main__':
    N,M = map(int,raw_input('input N,M:').split(','))  

    f[0][1] = 1
    used[0][1] = 1

    f[M][1] = dfs(M-1,N)+dfs(M-1,2)
    print('f[%d][1]:%d' %(M,f[M][1]))




