# -*- coding: utf-8 -*-
import os, sys, site

# for relative paths
here   = lambda x="": os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
parent = lambda x: os.path.abspath(os.path.join(x, os.pardir))

def load(venv_dir="venv"):
    # Virtualenv directory
    venv = os.path.join( parent( here() ), venv_dir)        
    # Add the app's directory to the PYTHONPATH
    sys.path.append(here())
    sys.path.append(parent(here()))
    # If virtual env exists
    if os.path.isdir(venv):      
        # Determine python packages
        major, minor = sys.version_info[0:2]
        sitepackages = '{venv}/local/lib/python{major}.{minor}/site-packages'
        sitepackages = sitepackages.format(venv=venv, major=major, minor=minor)          
        # Add the site-packages of the chosen virtualenv to work with
        if os.path.isdir(sitepackages):
            site.addsitedir(sitepackages)
            # Activate your virtual env
            activate_env=os.path.expanduser("%s/bin/activate_this.py" % venv)
            execfile(activate_env, dict(__file__=activate_env))    
    # Vendor directory
    path = "%s/vendor/" % ( parent(here()) ) 
    # Load all librairies in the vendor directory
    for directory in os.listdir(path): sys.path.append(path + directory) 
