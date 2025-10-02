import os
import sys

def data_pipe():
    import importlib.util

    script_paths = [
       "/workspaces/Proyecto-Lab-2/Data/etl/sor_to_rdz/ingesta.py",
       "/workspaces/Proyecto-Lab-2/Data/etl/rdz_to_cdz/curado.py",
       "/workspaces/Proyecto-Lab-2/src/predictions & training/predecir.py"
    ]

    for script_path in script_paths:
        script_dir = os.path.dirname(script_path)
        sys.path.insert(0, script_dir)  # Add script's directory to sys.path

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

data_pipe()