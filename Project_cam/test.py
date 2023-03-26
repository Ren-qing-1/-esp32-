import machine


# 按键中断回调函数
def key_callback(pin):
    print("按键中断")


# 触发按键中断函数 高电平触发
def key_trigger():
    # 初始化按键引脚
    key_pin = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
    # 初始化中断
    key_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=key_callback)
