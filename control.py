'''

	Synopsis: Script to run the control algorithm.
	Author: Nikhil Venkatesh
	Contact: mailto:nikv96@gmail.com

'''

# Dronekit Imports
from time import time
from dronekit import VehicleMode

# Common Library Imports
from flight_assist import send_velocity
import pid


# Python Imports
import math
import random
import time


#udp
import socket
import time
#创建socket对象
#SOCK_DGRAM  udp模式
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
focus_add="#TPUM2wZMC015D"
focus_sub="#TPUM2wZMC025E"

# Global Variables
x_pid = pid.pid(0.12, 0.005, 0.1, 50)
y_pid = pid.pid(0.12, 0.005, 0.1, 50)
hfov = 0.6
hres = 640
vfov = 0.6
vres = 640
tage_number = 0
# if_FIND_TARGET = False  # 是否发现目标，如果是已经发现目标，就不会触发向上飞的指令
max_none_number_pid = 80  # 调节的最大次数,超过就直接投弹判断失败
none_number_pid = 0
number_find = 0  # 检测目标的次数


#在高度变化时候手动触发变焦，帮助拍摄更加清晰的图片。
def change_fcus():
    # s.sendto(focus_add.encode(),("192.168.1.144",9003))
    # s.sendto(focus_sub.encode(),("192.168.1.144",9003))
    pass





def pixels_per_meter(fov, res, alt):
    # return ( ( alt * math.tan(math.radians(fov/2)) ) / (res/2) )
    # return alt*0.00296875
    # return alt*0.0005512 #1920
    return alt*0.00077639  # 1920

# t投弹
def DropBomb(vehicle):
    #send_velocity(vehicle, 0, 0, 0, 2)
    # time.sleep(0.5)

    #change by vertin
    #vehicle.channels.overrides = {'7': 1900}
    print("DUUUUUUU")
    #----------------


def land(vehicle, target, if_FIND_TARGET):
    # global if_FIND_TARGET
    global none_number_pid
    none_number_pid = none_number_pid+1
    if(none_number_pid > max_none_number_pid):  # 寻找目标最大次数达到 识别失败，直接投弹
        return True

    if(if_FIND_TARGET == True):
        send_velocity(vehicle, 0, 0, 0.5, 5)  # 找到目标，下降飞行寻找目标
        print("下降")
        return True
    if(if_FIND_TARGET == False):
        # 没有找到目标现在,随机移动一下，模型就可能寻找到目标
        x = random.randrange(0, 50)/100-0.25  # 生成的数字-0.1-0.1
        y = random.randrange(0, 50)/100-0.25  # 生成的数字
        send_velocity(vehicle, x, y, 0, 5)
        print("未找到目标")
        return False


# 移动到目标过程中的控制
# def move_to_target(vehicle, target):

#     x = target[0]
#     y = target[1]
#     dis_pix = math.sqrt(x**2 + y**2)  # 目标与无人机的 像素距离

#     alt = vehicle.location.global_relative_frame.alt
#     px_meter_x = pixels_per_meter(hfov, hres, alt)
#     px_meter_y = pixels_per_meter(vfov, vres, alt)

#     x *= px_meter_x
#     y *= px_meter_y

#     vx = x_pid.get_pid(x, 0.5)
#     vy = y_pid.get_pid(y, 0.5)

#     print("x = " + str(x))
#     print("vx = " + str(vx))
#     print("y = " + str(y))
#     print("vy = " + str(vy))

#     # pid 计算完成参数
#     global tage_number
#     tage_number = tage_number+1  # 目标在0.5米的次数
#     if(vehicle.location.global_relative_frame.alt <= 12 and dis_pix < tage_number*5):
#         send_velocity(vehicle, vx, vy, 0, 1)
#         DropBomb(vehicle)
#         return True

#     if(dis_pix > 250):
#         send_velocity(vehicle, vx, vy, 0, 5)
#         global number_find
#         number_find = number_find+1
#         if(number_find > 3):  # 检测到三次后就不会上升
#             global if_FIND_TARGET
#             if_FIND_TARGET = True
#         return False

#     else:  # 已经发现目标
#         if(vehicle.location.global_relative_frame.alt > 8.5):
#             send_velocity(vehicle, vx, vy, 0.5, 5)
#             change_fcus()
#             # 下降一次之后，我们发现目标的这个次数就重置
#             print("下降")
#             tage_number = 0
#             return False
#         else:
#             send_velocity(vehicle, vx, vy, 0, 5)
#             return False


if __name__ == "__main__":
    x = 640
    y = 20
    alt = 10

    px_meter_x = pixels_per_meter(hfov, hres, alt)
    px_meter_y = pixels_per_meter(vfov, vres, alt)
    print(px_meter_x, px_meter_y)

    x *= px_meter_x
    y *= px_meter_y

    vx = x_pid.get_pid(x, 0.5)
    vy = y_pid.get_pid(y, 0.5)

    print("x = " + str(x))
    print("vx = " + str(vx))
    print("y = " + str(y))
    print("vy = " + str(vy))
