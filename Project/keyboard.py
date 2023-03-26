import time
from machine import Pin
from machine import Timer


# 4*4矩阵键盘类
class Keyboard():
    def __init__(self):
        # 初始化引脚
        self.key_down = ""
        self.row1 = Pin(19, Pin.OUT)
        self.row2 = Pin(18, Pin.OUT)
        self.row3 = Pin(5, Pin.OUT)
        self.row4 = Pin(17, Pin.OUT)
        self.row_list = [self.row1, self.row2, self.row3, self.row4]

        self.col1 = Pin(16, Pin.IN, Pin.PULL_DOWN)
        self.col2 = Pin(4, Pin.IN, Pin.PULL_DOWN)
        self.col3 = Pin(2, Pin.IN, Pin.PULL_DOWN)
        self.col4 = Pin(15, Pin.IN, Pin.PULL_DOWN)
        self.col_list = [self.col1, self.col2, self.col3, self.col4]

        # 定义键盘名称
        self.key = [
            ['1', '2', '3', 'A'],
            ['4', '5', '6', 'B'],
            ['7', '8', '9', 'C'],
            ['*', '0', '#', 'D']
        ]

        # 初始化定时器
        self.timer1 = Timer(0)
        self.timer_init()

    # 定时器初始化
    def timer_init(self):
        print("定时器初始化")
        self.timer1.init(period=250, mode=Timer.PERIODIC, callback=self.key_scan)

    # 检测看按键引脚电平
    def key_scan(self, event):
        # 清空上一次键盘输入
        # self.key_down = ""
        for i, row in enumerate(self.row_list):
            for temp in self.row_list:
                temp.value(0)
            row.value(1)
            time.sleep_ms(10)
            for j, col in enumerate(self.col_list):
                if col.value() == 1:
                    # print(self.key_down)
                    self.key_down = self.key[i][j]
                else:
                    pass


if __name__ == '__main__':
    # key_scan()
    keyboard = Keyboard()
    while True:
        print(keyboard.key_down)
        time.sleep(1)
