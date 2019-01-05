import jsbeautifier
import sys
import os
import random

filename = sys.argv[2]+"-"+str(os.times()[4])+"-"+str(random.randint(1,99999))
os.system("copy NUL "+filename)
res = jsbeautifier.beautify_file(sys.argv[1])
with open(filename,'w') as f:
    f.write(res)

print filename
