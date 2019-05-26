#!/usr/bin/python3


import sys
import shutil
import os


#template="/home/local/jttoivon/kurssit/dap/project_template"
template = os.path.dirname(sys.argv[0]) + "/exercise_template"
try:
    name=sys.argv[1]
except IndexError:
    print("Given exercise name as parameter")
    print('Usage: newex.py "tehtavan nimi"')
    sys.exit(1)
    
parts=name.split()
dst="e00_" + "_".join(parts)
src="_".join(parts)
capname="".join(map(lambda x : x.capitalize(), parts))
print(dst)
shutil.copytree(template, dst)

fsrc=dst + "/src/" + src + ".py"
ftest=dst + "/test/test_" + src + ".py"
os.rename(dst+"/src/function.py", fsrc)
os.rename(dst+"/test/test_function.py", ftest)

# Insert the load command
module_name="src.%s" % src
replacement=r"""module_name="%s"\n%s = load(module_name, "%s")""" % (module_name, src, src)
command="""sed -i '/^ = load(/s/.*/%s/' %s""" % (replacement, ftest)
print(command)
os.system(command)

# Insert the name of the class
command="""sed -i "/^class /s/.*/class %s(unittest.TestCase):/" %s""" % (capname, ftest)
print(command)
os.system(command)

func=r"""def %s():
    return "hello"
""" % src
func=func.replace("\n", r"\n")

command="""sed -i '3i%s' %s""" % (func, fsrc)
print(command)
os.system(command)

command="""sed -i '/pass/s/.*/    print(%s())/' %s""" % (src, fsrc)

print(command)
os.system(command)

print("Created files:", ftest, fsrc)
