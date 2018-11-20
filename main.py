from  subprocess import Popen, PIPE,check_output,CalledProcessError
import sys
from time import sleep
from os import system
test = Popen(["adb","shell","getevent","-l"],stderr=PIPE)

print("Output: \n{}\n".format(test.communicate()[0].decode('utf-8')))


"""
command = "getevent -l".encode('utf-8')
print(command)
input = test.communicate(command)
output = test.communicate()[0].decode('utf-8')

try:
    error = test.communicate()[1]
    print(error)
except(ValueError):
    print("No Error Found")

sys.stdout.flush()
output = test.communicate()[0].decode('utf-8')
test.communicate("exit")
print(output)
"""