import os
import argparse

# path to the URScriptToPulseConverter
package_path = os.path.dirname(os.path.abspath(''))

# Default parameters
NAME = 'path'
HOST = '127.0.0.1:8081'
SAVE_PATH = os.path.join(package_path, 'processedPrograms')
FILE_PATH = os.path.join(package_path, 'RoboDKPrograms/Path.script')

arguments = argparse.ArgumentParser()
arguments.add_argument("-n", "--name", type=str, default=NAME,
    help="program name")
arguments.add_argument("-s", "--save_path", type=str, default=SAVE_PATH,
    help="save program in special folder")
arguments.add_argument("-i", "--initial_program", type=str, default=FILE_PATH,
    help="program name")
arguments.add_argument("-o", "--host_name", type=str, default=HOST, help="robot host name")