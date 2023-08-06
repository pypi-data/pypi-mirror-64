import os
import pathlib
import argparse

# path to the URScriptToPulseConverter
package_path = pathlib.Path(__file__).parents[1]

# Default parameters
NAME = 'path'
HOST = '127.0.0.1:8081'
SAVE_PATH = os.path.join(package_path, 'processedPrograms')

arguments = argparse.ArgumentParser()
arguments.add_argument("-n", "--name", type=str, default=NAME,
    help="program name")
arguments.add_argument("-s", "--save_path", type=str, default=SAVE_PATH,
    help="save program in special folder")
arguments.add_argument("-i", "--initial_program", type=str, help="program name")
arguments.add_argument("-o", "--host_name", type=str, default=HOST, help="robot host name")