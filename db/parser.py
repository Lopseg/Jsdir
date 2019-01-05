import jsbeautifier
import sys
import os
import random

filename = sys.argv[2]+"-"+str(os.times()[4])+"-"+str(random.randint(1,99999))+".txt"
os.system("copy NUL "+filename)

parser = open(sys.argv[1],"r")

body = parser.read().split('\r\n\r\n')
with open(filename,'w') as f:
    f.write(body[1])
parser.close()

res = jsbeautifier.beautify_file(filename)
with open(filename,'w') as f:
    f.write(res)

print filename
