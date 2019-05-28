#!/usr/bin/python3

import getopt
import sys
import shutil
import os

src_template="""#!/usr/bin/env python3

def %s():
    return "hello"

def main():
    print(%s())

if __name__ == "__main__":
    main()
"""

test_template="""#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock

from tmc import points
from tmc.utils import load, get_out, patch_helper, spy_decorator

module_name = "src.%s"
%s = load(module_name, '%s')
main = load(module_name, "main")
ph = patch_helper(module_name)

@points('%s')
class Test%s(unittest.TestCase):
    
    def test_first(self):
        self.assertEqual("", "", msg="fill me")


if __name__ == '__main__':
    unittest.main()
"""

usage="""Usage: newex.py [-p partnumber ] [ -e exercisenumber ] 'name of exercise'
-p\tPart number, default is 0
-e\tExercise number, default is 0
"""


def write_src(dst, exname):
    try:
        os.makedirs(os.path.join(dst, "src"))
    except FileExistsError:
        pass
    filename=os.path.join(dst, "src", exname) + ".py"
    with open(filename, "w") as f:
        f.write(src_template % (exname, exname))
        
def write_test(dst, exname, points, capname):
    filename=os.path.join(dst, "test", "test_%s.py" % exname)
    with open(filename, "w") as f:
        f.write(test_template % (exname, exname, exname, points, capname))

optlist, args = getopt.getopt(sys.argv[1:], "p:e:h", ["part=", "exercise=", "help"])
args = [sys.argv[0]] + args
template = os.path.join(os.path.dirname(args[0]), "exercise_template")
try:
    name=args[1]
except IndexError:
    print("Given exercise name as parameter")
    print(usage)
    sys.exit(1)
    
parts = name.split()
exname = "_".join(parts)
capname="".join(map(lambda x : x.capitalize(), parts))
part_number = 0
exercise_number = 0
for opt, arg in optlist:
    if opt in ["-p", "--part"]:
        part_number = int(arg)
    elif opt in ["-e", "--exercise"]:
        exercise_number = int(arg)
    else:
        print(usage)
        sys.exit(0)
        
dst = "e%02i_%s" % (exercise_number, exname)
points = 'p%02i-%02i.1' % (part_number, exercise_number)

shutil.copytree(template, dst)

write_src(dst, exname)
write_test(dst, exname, points, capname)
print("Created exercise %s" % dst)

