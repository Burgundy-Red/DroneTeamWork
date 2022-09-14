from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative, Command
from pymavlink import mavutil

# Python Imports
import time
import math
import logging

# def function import
from flight_assist import *


def above_target(x, y):
    """
    判断飞到目标上空
    Args:
        x(float): 
        y(float):
    Returns:
        result(bool):
    """
    result = False
    if IMAGEWIDTH/2 * 0.9 <= x <= IMAGEWIDTH/2 * 1.1 and IMAGEHEIGHT/2 * 0.9 <= y <= IMAGEHEIGHT/2 * 1.1:
        result = True
    return result

def calulate_yaw(point, relative=False):
    """
    由目标框中心点与图像中心点的相对位置，计算 yaw 角
    z 轴指向下, 根据右手坐标系X轴水平向前，Y轴水平向右
    Args:
        point(tuple): (320 - abs_x, abs_y - 640)相对位置
        relative(bool): 已经是相对坐标
    Returns:
        yaw(float): yaw 角( 0 <= yaw <= 360)
    """
    x, y = point if relative else (IMAGEHEIGHT/2- point[1], point[0] - IMAGEWIDTH/2)
    l = math.sqrt(x * x + y * y)
    a = math.acos(x / l) if l > 1e-8 else 0;
    ret = a * 180.0 / math.pi
    if (y < 0):
        ret = 360 - ret
    return ret


def set_vehicle_yaw(vehicle, yaw):
    """
    通过condition_yaw 设置 yaw 角
    转动时防止无人机高度变化，添加函数监视，并在高度下降时发送指令。
    TODO: 添加rangefinder监听函数
    Args:
        vehicle(vehicle instance):
        yaw(float): 角度
    Returns:
    """
    altitude = vehicle.location.global_relative_frame.alt
    def keep_altitude_callback(self, name, v):
        if v < altitude * 0.9:
            self.simple_takeoff(altitude)

    vehicle.add_attribute_listener("location.global_relative_frame")
    condition_yaw(vehicle, yaw, relative=False)
    vehicle.remove_attribute_listener("location.global_relative_frame")

    
if __name__ == '__main__':

    import argparse  
    parser = argparse.ArgumentParser(description='Control Copter and send commands in GUIDED mode ')
    parser.add_argument('--connect', 
                       help="Vehicle connection target string. If not specified, SITL automatically started and used.")
    args = parser.parse_args()

    connection_string = args.connect
    sitl = None

    if not connection_string:
        import dronekit_sitl
        sitl = dronekit_sitl.start_default()
        connection_string = sitl.connection_string()


    # Connect to the Vehicle
    print('Connecting to vehicle on: %s' % connection_string)
    vehicle = connect(connection_string, wait_ready=True)
    vehicle.home_location = vehicle.location.global_frame
    targetLocation = vehicle.home_location

    arm_and_takeoff(vehicle, 10)
    
    point = [(0,0), (1280,0), (1280,640), (0,640), (640,320)]
    for p in point[:2]:
        yaw = calulate_yaw(p, relative=False)
        # set_vehicle_yaw(vehicle, yaw)
        
        # dronekit-sitl does not automatically add a virtual gimbal
        # vehicle.gimbal.target_location(targetLocation)
        set_vehicle_velocity_yaw(vehicle, yaw, duration=20)


    vehicle.gimbal.target_location(vehicle.location.global_relative_frame)
    print("Setting LAND mode...")
    vehicle.mode = VehicleMode("LAND")
    #Close vehicle object before exiting script
    print("Close vehicle object")
    vehicle.close()

    # Shut down simulator if it was started.
    if sitl is not None:
        sitl.stop()

    print("Completed")
    
    
