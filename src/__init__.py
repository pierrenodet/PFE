import os, sys, inspect

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
cmd_folder = cmd_folder[0:cmd_folder.find("src")]
sys.path.append(cmd_folder)
sys.path.append(cmd_folder+"src/")

import make_data
import pre_process_data
import clean_data
import make_trace
import make_trace_bis
