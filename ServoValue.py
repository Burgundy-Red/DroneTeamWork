import threading
from pymavlink import mavutil

class ServoValue:
    """
    为 RC 的 PWM 提供读写保护
    """
    _lock = threading.Lock()

    def __init__(self):
        self._channels_5_8 = [1500, 1500, 1500, 1500]

    @staticmethod
    def change_channel_value(vehicle, channel, v):
        """
        Args:
            channel(int): 6通道: pitch 7通道: yaw
            num(int): 1100 <= num <= 1900
        Returns:
        """
        try:
            v = max(1100, min(v, 1900))
            msg = vehicle.message_factory.command_long_encode(
                0, 0,
                mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
                0,
                channel,
                v,
                0,
                0,
                0, 0, 0)

            vehicle.send_mavlink(msg)
        except Exception as e:
            print(e)

    @property
    def c5(self):
        with ServoValue._lock:
            return self._channels_5_8[0]

    @property
    def c6(self):
        with ServoValue._lock:
            return self._channels_5_8[1]

    @property
    def c7(self):
        with ServoValue._lock:
            return self._channels_5_8[2]

    @property
    def c8(self):
        with ServoValue._lock:
            return self._channels_5_8[3]

    # def set_servo_value_5_8(self, m):
    #     with ServoValue._lock:
    #         self._channels_5_8[0] = m.servo5_raw
    #         self._channels_5_8[1] = m.servo6_raw
    #         self._channels_5_8[2] = m.servo7_raw
    #         self._channels_5_8[3] = m.servo8_raw

    @c5.setter
    def c5(self, v):
        v = max(1100, min(v, 1900))
        with ServoValue._lock:
            self._channels_5_8[0] = v

    @c6.setter
    def c6(self, v):
        v = max(1100, min(v, 1900))
        with ServoValue._lock:
            self._channels_5_8[1] = v

    @c7.setter
    def c7(self, v):
        v = max(1100, min(v, 1900))
        with ServoValue._lock:
            self._channels_5_8[2] = v

    @c8.setter
    def c8(self, v):
        v = max(1100, min(v, 1900))
        with ServoValue._lock:
            self._channels_5_8[3] = v
