'''
1.Suggest use "subprocess" to replace "os".
2.Subprocess fork a new subprocess to execUte cmd, and very easy to get retcode and result
of the shell cmd.
'''

def py_shell_os():
   import os
  
   retcode = os.system("echo \'hello world\' ")
   retcode = os.system("ls")
   retcode = os.system("cat test.sh")
   retcode = os.system("sh test.sh")


# output[0] is output of cmd
# output[1] is error info of cmd
def py_shell_subprocess():
   import subprocess

   p = subprocess.Popen(['ls','-'], stdout=subprocess.PIPE)

   output = p.communicate()

   print(output[0])
   print(output[1])




if __name__ == '__main__':
    py_shell_subprocess()


