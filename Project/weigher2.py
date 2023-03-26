from machine import Pin, ADC  # 引入ADC模块
from time import sleep


# 判断饲料槽内是否是满的
def is_full():
    # DO = machine.Pin(33)
    # 读取模拟电压值
    AO = Pin(32)

    pot = ADC(Pin(33))  # 定义34脚为ADC脚(在32~39上可用)，可以读取模拟电压
    pot.width(ADC.WIDTH_12BIT)  # 读取的电压转为0-4096；ADC.WIDTH_9BIT：0-511
    pot.atten(ADC.ATTN_11DB)  # 衰减设置范围：输入电压0-3.3v

    pot_value_1 = pot.read() // 4  # 使读取的电压变为0-1024
    sleep(0.5)  # 等待0.5s
    pot_value_2 = pot.read() // 4  # 使读取的电压变为0-1024
    sleep(0.5)  # 等待0.5s
    pot_value_3 = pot.read() // 4  # 使读取的电压变为0-1024

    if pot_value_1 and pot_value_2 and pot_value_3:  # 如果1s内三次电压都有值则表示饲料槽内还有饲料
        print('pot_value:', pot_value_1, pot_value_2, pot_value_3)
        return True
    else:
        return False


if __name__ == '__main__':
    is_full()
