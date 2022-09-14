import shutil
import random
import os
import sys
import time
import redis
import logging
import argparse
from pathlib import Path
from func_timeout import FunctionTimedOut, func_timeout

# Dronekit imports
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
from dronekit_sitl import SITL
from pymavlink import mavutil

# Helper Libraries Imports
import control
from flight_assist import *
from util import *

redis_conn = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def main(args):
    """
    Args:
        connect_string(str): usb, tcp, udp
        altitude(int):
        coordfile(str): coordination file
    Returns:
    """
    logger = logging.getLogger()
    connect_string = args.connect_string
    if not connect_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connect_string = sitl.connection_string()
        logging.debug("Starting a simulator.")

    
    try:
        print('Connecting to vehicle on: %s' % connect_string)
        vehicle = connect(connect_string, wait_ready=True, baud=115200)
        

        vehicle.mode = VehicleMode("GUIDED")
        while True:
            if (vehicle.mode == "GUIDED"):
                break
            time.sleep(0.1)


        # TODO 进程保存图片
        # add_velocity_message_listener(vehicle, None)
        # attritutes = ["gimbal",]
        # add_attributes_listener_init(vehicle, attritutes, None)


        # 飞到一定高度
        altitude = args.altitude
        arm_and_takeoff(vehicle, altitude)


        # 手动控制 按q退出
        direction_command_set = ["k", "j", "h", "l", "n", "m"] # 上下左右前后
        gimbal_command_set = ["i", "u", "y", "o"]              # 上下左右
        command = "w"
        while command != "q":
            try:
                # command = func_timeout(1, lambda: input("Command: "))
                command = input("Command: ")
            except FunctionTimedOut:
                command = "w"

            if command in direction_command_set:
                constant_speed_flight_to(vehicle, command, direction_command_set)
            elif command in gimbal_command_set:
                change_gimbal_angle(vehicle, command, gimbal_command_set)
            else:
                # 原地不动
                constant_speed_flight_to(vehicle, "w")
            

        # 降落到出发点
        print("Returning to Launch")
        vehicle.mode = VehicleMode("RTL")
        vehicle.close()


    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    args = get_arguments()
    logging = get_logger(args, mode='w')
    main(args)
