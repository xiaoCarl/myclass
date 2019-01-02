/*
1.定义状态：
Dp[i][j]  表示传了i次在j的手中
 
第j个人是如何得到球发现：上一次球在j+1和j-1在传过来
Dp[i][j]=dp[i-1][j-1]+dp[i-1][j+1]
 
当j=1   相邻两个为n和2
Dp[i][j]=dp[i-1][n]+dp[i-1][2]
当j=n   相邻两个为n-1和1
Dp[i][j]= dp[i-1][n-1]+dp[i-1][1]
 
 
初值：
Dp[0][1]=1;

*/

#include<stdio.h>

int N,M,f[50][50];
int main()
{
   printf("input N,M:");
   scanf("%d,%d",&N,&M);
  
   f[0][1]=1;
   for(int i=1;i<=M;i++)
   {
      for(int j=1;j<=N;j++)
      {
         if (j==1) f[i][j]=f[i-1][N]+f[i-1][2];     
         else if (j==N)  f[i][j]=f[i-1][1]+f[i-1][N-1];
         else f[i][j]=f[i-1][j-1]+f[i-1][j+1];
       }
   }
   printf("f[%d][1]:%d\n",M,f[M][1]); 
   return 0;
}

