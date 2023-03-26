from machine import freq
from hx711 import HX711


# 称重函数
def get_weight():
    # 设置通信频率
    freq(160000000)
    # 计算参数
    num = 499
    # 初始重量
    start_weight = 1008.857

    type_128 = HX711(d_out=21, pd_sck=22)
    num_128 = type_128.read()
    type_128.channel = HX711.CHANNEL_A_64
    num_64 = type_128.read()

    weight = ((num_64 * 2 + num_128) / 2 / num) - start_weight

    return round(weight)


if __name__ == '__main__':
    get_weight()
