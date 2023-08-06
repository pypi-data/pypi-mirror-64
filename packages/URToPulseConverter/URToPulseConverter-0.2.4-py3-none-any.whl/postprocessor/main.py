from .argsParser import arguments
from .converter.programParser import program_parser, read_file
from .converter.RobodkUR2Pulse import Postprocessor

def main() -> None:
    args = arguments.parse_args()

    postprocessor = Postprocessor(robothost=args.host_name)
    program = read_file(args.initial_program)

    program_parser(program, postprocessor)
    postprocessor.progSave(args.save_path, args.name, show_result=True)