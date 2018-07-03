# -*- coding: utf-8 -*-

#%% 

    # Add my utilities
#import sys
#util_path = 
sys.path.append("/home/batman/git/py2nb")
import py2nb

#import importlib.util
#spec = importlib.util.spec_from_file_location("module.name", )
#foo = importlib.util.module_from_spec(spec)
#spec.loader.exec_module(foo)
#foo.MyClass()
#import py2nb #as 
#py2nb.__file__
##from py2nb import python_to_notebook
from py2nb.tools import python_to_notebook

curr_path = r"/home/batman/git/util_ManageGitRepos/src/list_repos.py"
dest_path = r"/home/batman/git/util_ManageGitRepos/src/list_repos.ipynb"
assert os.path.exists(curr_path)

py2nb.tools.python_to_notebook(curr_path,dest_path)
#import sys
#script = sys.argv[0]

#py2nb.python_to_notebook(input_#filename, output_filename)

#dir(py2nb)