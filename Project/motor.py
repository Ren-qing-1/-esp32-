from machine import Pin, PWM
import time
import math


# 计算角度所对应的占空比
def compute(num):
    # 0度 0.5ms 1638
    # 45度 1.0ms 3276
    # 90度 1.5ms 4915
    # 135度 2.0ms 6553
    # 180度 2.5ms 8191

    return math.floor(((2/180*num)+0.5)/20*65535)


# 自定义旋转角度
# def main(start, end):
#     # 设定PWM对象和通信频率
#     p2 = PWM(Pin(13))
#     p2.freq(50)
#
#     start = compute(start)
#     end = compute(end)
#
#     if start < end:
#         for i in range(start, end, 10):
#             p2.duty_u16(i)
#             time.sleep_ms(2)
#     elif start > end:
#         for i in range(start, end, -10):
#             p2.duty_u16(i)
#             time.sleep_ms(2)
#
#     p2.deinit()

# 自定义旋转角度
def main(start):
    # 设定PWM对象和通信频率
    p2 = PWM(Pin(13))
    p2.freq(50)
    p1 = PWM(Pin(27))
    p1.deinit()

    start = compute(start)

    p2.duty_u16(start)


if __name__ == '__main__':
    main(45)
