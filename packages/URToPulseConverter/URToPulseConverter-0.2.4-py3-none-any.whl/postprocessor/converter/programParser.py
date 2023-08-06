import re

def read_file(file_path):
    """Read initial program"""
    with open(file_path, 'r') as program:
        program = open(file_path, "r")
        program = str(program.read())
        return program.split('\n')

def find_numbers(data: str):
    """Finds all numbers in single line"""
    diction = re.findall('([-+]?(?:\d+(?:\.\d*)?|\.\d+))', data)
    diction = [float(number) for number in diction]
    return diction

def find_word(word: str, data: str) -> bool:
    """Find word in line"""
    if word in data:
        return True
    else: return False

def program_parser(program: str, postprocessor) -> None:
    """ """
    for i, line in enumerate(program):
        if find_word('set_ref', line):
            postprocessor.set_ref_frame(line)

        if find_word('set_tcp', line):
            postprocessor.set_tcp(line)

        if find_word('speed_ms', line) and find_word('=', line):
            postprocessor.set_speed(line)

        if find_word('movel([', line) and find_word('movel([', program[i+1]):
            postprocessor.movej(line)
        elif find_word('movel([', line):
            postprocessor.movej(line)
            postprocessor.runPoses()

        if find_word('movej', line) and find_word('movej', program[i+1]):
            postprocessor.movej(line)
        elif find_word('movej', line):
            postprocessor.movej(line)
            postprocessor.runPoses()

        if find_word('movel(p', line) and find_word('movel(p', program[i+1]):
            postprocessor.movel(line)
        elif find_word('movel(p', line):
            postprocessor.movel(line)
            postprocessor.runPositions()

        if find_word("Set air valve on", line):
            postprocessor.open_gripper()

        if find_word("Set air valve off", line):
            postprocessor.close_gripper()

        if find_word("Sleep", line):
            t = find_numbers(line)
            postprocessor.sleep(*t)