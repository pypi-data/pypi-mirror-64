import os
import math
import time
import numpy as np

from .programParser import find_numbers, find_word
from .linalg import UR_2_Pose, Pose_2_TxyzRxyz, txyzRxyz_2_pose


class Postprocessor():
    """
    Generate program for Rozum Robotics robots like Pulse 75 or Pulse 90.

    Initial program is RoboDK generated program for Universal robot. That why we need to
    recalculate initial coordinates to the standart form (named - pose. 4x4 matrix) using UR_2_Pose function

    Should use Universal_Robots.py postprocessor with some changes.
    """
    PROG = ""
    PROG_EXT = 'py'
    TARGET_POSES = []
    TARGET_POSITIONS = []
    REF_FRAME = np.eye((4))
    TOOL_FRAME = np.zeros(6)
    SPEED_MS = 0.01

    def __init__(self, robothost: str):
        self.HOST = robothost
        self.progStart()


    def progSave(self, folder: str, progname: str, show_result: bool = False) -> None:
        """Save program in special folder"""
        progname = progname + '.' + self.PROG_EXT
        filesave = os.path.join(folder, progname)

        with open(filesave, 'w') as fid:
            fid.write(self.PROG)

        print('SAVED: %s\n' % filesave)
        # show result
        if show_result:
            # open file with default application
            os.startfile(filesave)


    def progStart(self) -> None:
        """Adds lines on the first place of your program"""
        self.addline("import time")
        self.addline('from pulseapi import *')
        self.addline(f"robot = RobotPulse('{self.HOST}')\n")


    def addline(self, newline: str) -> None:
        """Add a program line"""
        self.PROG = self.PROG + newline + '\n'


    def movel(self, line: str) -> None:
        """Recalculate UR coordinates to the standart form. """
        coordinates = np.array(find_numbers(line)[0:6])
        coordinates = UR_2_Pose(coordinates)
        coordinates = np.matmul(np.matmul(self.REF_FRAME, coordinates), np.linalg.inv(self.TOOL_FRAME))
        coordinates = np.matmul(self.REF_FRAME, coordinates)
        coordinates = Pose_2_TxyzRxyz(coordinates)
        XYZ = [round(value, 4) for value in coordinates[:3]]
        RXYZ = [round(value, 3) for value in coordinates[3:]]
        self.TARGET_POSITIONS.append(f'{XYZ}, {RXYZ}')


    def movej(self, line: str) -> None:
        coordinates = find_numbers(line)[0:6]
        coordinates = [round(math.degrees(coord), 2) for coord in coordinates]
        self.TARGET_POSES.append(f'{coordinates}')


    def runPositions(self, speed=None, velocity=None, acceleration=None) -> None:
        self.addline("target_position = [")
        for pos in self.TARGET_POSITIONS:
            self.addline(f"     position({pos}),")
        self.addline("]")
        self.TARGET_POSITIONS.clear()

        if isinstance(speed, (int, float)):
            self.addline(f'robot.run_positions(target_position, speed={speed}, motion_type=MT_LINEAR)')
            self.addline('robot.await_stop()')
        elif isinstance(velocity, (int, float)) and isinstance(acceleration, (int, float)) and speed == None:
            self.addline(f'robot.run_positions(target_position, velocity={velocity}, acceleration={acceleration}, motion_type=MT_LINEAR)')
            self.addline('robot.await_stop()')
        elif isinstance(velocity, (int, float)) and isinstance(acceleration, (int, float)) and isinstance(speed, (int, float)):
            self.addline(f'robot.run_positions(target_position, tcp_max_velocity={self.SPEED_MS}, motion_type=MT_LINEAR)')
            self.addline('robot.await_stop()')
        elif speed==None and velocity==None and acceleration==None:
            self.addline(f'robot.run_positions(target_position, tcp_max_velocity={self.SPEED_MS},  motion_type=MT_LINEAR)')
            self.addline('robot.await_stop()')
        else:
            raise AssertionError("Incorrect introduced parameters. Enter only speed parameter or velocity and acceleration")


    def runPoses(self, speed=None, velocity=None, acceleration=None):
        self.addline("target_poses = [")
        for pos in self.TARGET_POSES:
            self.addline(f"     pose({pos}),")
        self.addline("]")
        self.TARGET_POSES.clear()

        if isinstance(speed, (int, float)):
            self.addline(f'robot.run_poses(target_poses, speed={speed}, motion_type=MT_JOINT)')
            self.addline('robot.await_stop()')
        elif isinstance(velocity, (int, float)) and isinstance(acceleration, (int, float)) and speed == None:
            self.addline(f'robot.run_poses(target_poses, velocity={velocity}, acceleration={acceleration}, motion_type=MT_JOINT)')
            self.addline('robot.await_stop()')
        elif isinstance(velocity, (int, float)) and isinstance(acceleration, (int, float)) and isinstance(speed, (int, float)):
            self.addline(f'robot.run_poses(target_poses, tcp_max_velocity={self.SPEED_MS}, motion_type=MT_JOINT)')
            self.addline('robot.await_stop()')
        elif speed==None and velocity==None and acceleration==None:
            self.addline(f'robot.run_poses(target_poses, tcp_max_velocity={self.SPEED_MS}, motion_type=MT_JOINT)')
            self.addline('robot.await_stop()')
        else:
            raise AssertionError("Incorrect introduced parameters. Enter only speed parameter or velocity and acceleration")


    def set_tcp(self, line):
        """Set TCP frame
            :param line: line with tcp coordinates from UR program
        """
        self.TOOL_FRAME = np.array(find_numbers(line))
        self.TOOL_FRAME = UR_2_Pose(self.TOOL_FRAME)
        self.TOOL_FRAME = Pose_2_TxyzRxyz(self.TOOL_FRAME)
        x,y,z,r,p,w= self.TOOL_FRAME
        self.addline(f"robot.change_tool_info(tool_info(position([{x},{y},{z}], [{r},{p},{w}])))")
        ########################################
        self.TOOL_FRAME = txyzRxyz_2_pose(self.TOOL_FRAME)


    def set_ref_frame(self, positions):
        """Set reference frame position"""
        self.REF_FRAME = np.array(find_numbers(positions))
        self.REF_FRAME = UR_2_Pose(self.REF_FRAME)
        self.REF_FRAME = Pose_2_TxyzRxyz(self.REF_FRAME)
        x, y, z, r, p, w = self.REF_FRAME
        self.addline(f"robot.change_base(position([{self.REF_FRAME[:3]}], [{self.REF_FRAME[3:]}]))")


    def open_gripper(self):
        self.addline('robot.open_gripper()')


    def close_gripper(self):
        self.addline('robot.close_gripper()')


    def set_speed(self, line):
        """
        Set TCP speed, meters per second
        """
        self.SPEED_MS = find_numbers(line)[0]

        if float(self.SPEED_MS) > 2:
            raise AssertionError('Speed is too height. Set it lower then 2 ms')
        self.addline(f'speed_ms = {self.SPEED_MS}')

    def sleep(self, time):
        self.addline(f"time.sleep({time})")