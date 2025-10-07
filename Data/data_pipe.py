import os
import sys


# script_paths = [
#        "/workspaces/Proyecto-Lab-2/Data/etl/sor_to_rdz/ingesta.py",
#        "/workspaces/Proyecto-Lab-2/Data/etl/rdz_to_cdz/curado.py",
#        "/workspaces/Proyecto-Lab-2/src/predictions & training/predecir.py"
#     ]

current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = current_dir.rsplit('Proyecto-Lab-2', 1)[0] + 'Proyecto-Lab-2/'
os.chdir(current_dir)
print(current_dir)

sys.path.insert(0, current_dir)


from la_libreria.authentication import Credentials
from la_libreria.connectors import MySQLConnector

from ..Data.etl.sor_to_rdz.ingesta import *
from ..Data.etl.rdz_to_cdz.curado import *
from ..src.predictions_and_training.predecir import *

sys.path.pop(0)









def data_pipe():
    import importlib.util

    for script_path in script_paths:
        script_dir = os.path.dirname(script_path)
          # Add script's directory to sys.path

        if not os.path.isfile(script_path):
            print(f"File not found: {script_path}")
            sys.path.pop(0)
            continue
        module_name = os.path.splitext(os.path.basename(script_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        if spec is None:
            print(f"Could not load spec for {script_path}")
            sys.path.pop(0)
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            print(f"Executed {script_path}")
        except Exception as e:
            print(f"Error executing {script_path}: {e}")
        finally:
            sys.path.pop(0)  # Clean up sys.path
