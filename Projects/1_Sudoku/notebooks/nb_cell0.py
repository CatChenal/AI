import os
import sys
from pathlib import Path

print('Python: {}; sys.prefix: {}\n'.format(sys.version, sys.prefix))
print('Currrent dir:', Path.cwd())


# TODO: convert os. code to work with Path
def add_to_sys_path(this_path, up=False):
    """
    Prepend this_path to sys.path.
    If up=True, path refers to parent folder (1 level up).
    """
    for p in sys.path:
        p = os.path.abspath(p)
    if up:
        newp = os.path.abspath(os.path.join(this_path, '..'))
    else:
        newp = os.path.abspath(this_path)
        
    if this_path not in (p, p + os.sep):
        print('Path added to sys.path: {}'.format(newp))
        sys.path.insert(0, newp)
        
# if notebook inside another folder, eg ./notebooks:
up =  os.path.abspath(os.path.curdir).endswith('notebooks')
add_to_sys_path(os.path.curdir, up)

if up:
    DIR_IMG = Path.cwd().parent.joinpath('Images')
else:
    DIR_IMG = Path.cwd().joinpath('Images')
if not DIR_IMG.exists():
    Path.mkdir(DIR_IMG)
    
    
import numpy as np
import pandas as pd
pd.set_option("display.max_colwidth", 200)

import matplotlib as mpl
import matplotlib.pyplot as plt

from pprint import pprint as pp

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from IPython.display import HTML, Markdown, IFrame, Image

#display(HTML("<style>.container { width:100% !important; }</style>"))

def new_section(title):
    style = "text-align:center;background:#c2d3ef;padding:20px;color:#ffffff;font-size:3em;width:98%"
    return HTML('<div style="{}">{}</div>'.format(style, title))

def filter_dir(obj, start_with_str='_', exclude=True):
    return [d for d in dir(obj) if not d.startswith(start_with_str) == exclude]

import inspect

def get_mdl_pkgs(alib):
    "Inspect module hierarchy on two levels ony."
    pkgs = {}
    for name, mdl in inspect.getmembers(alib, inspect.ismodule):
        print('\n{:>13} : {}'.format(mdl.__name__, filter_dir(mdl)))
        for mdl_name, mdl_sub in inspect.getmembers(mdl, inspect.ismodule):
            if mdl_sub.__doc__:
                print('\n{:>20} : {}'.format(mdl_name, mdl_sub.__doc__.strip()))

%load_ext autoreload
%autoreload 2 