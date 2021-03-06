import unittest
import pythran
import os
from imp import load_dynamic

class CompileTest(object):
    def __init__(self, module_name):
        self.module_name=module_name
        
    def __call__(self, check_output=False):
        module_path=os.path.join(os.path.dirname(__file__),"rosetta",self.module_name+".py")
        print self.module_name

        specs = { "test": [] }
        module_code = file(module_path).read()
        if "unittest.skip" in module_code:
            return self.skipTest("Marked as skipable")
        mod = pythran.cxx_generator(self.module_name, module_code, specs)
        pymod=load_dynamic(self.module_name, pythran.compile(os.environ.get("CXX","c++"), mod, check=False))
        if check_output:
            res = getattr(pymod,"test")()
            compiled_code=compile(file(module_path).read(),"","exec")
            env={}
            eval(compiled_code, env)
            ref=eval("test()",env)
            if ref != res:
              print ref, res

class TestCase(unittest.TestCase):
    pass

import glob
for f in glob.glob(os.path.join(os.path.dirname(__file__),"rosetta", "*.py")):
    name=os.path.splitext(os.path.basename(f))[0]
    setattr(TestCase,"test_"+name, CompileTest(name))

if __name__ == '__main__':
    unittest.main()
