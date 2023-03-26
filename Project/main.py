import oled  # 导入oled显示屏模块
import time  # 导入时间模块
import keyboard  # 导入矩阵键盘模块
import motor  # 导入舵机模块
import weigher  # 导入称重模块
import weigher2  # 导入薄膜压力传感器模块
import wifi  # 导入wifi收发模块
import mqtt  # 导入mqtt服务器连接模块
import blue  # 导入蓝牙收发模块
import _thread  # 导入多线程模块
import utime  # 导入获取本地时间模块
import buzzer  # 导入蜂鸣器模块
import mp3  # 导入MP3模块
import json  # 导入json操作库

# 参数初始化
key = ""  # 初始化键盘输入为空
top = ['00:00', 'off']  # 状态栏显示数组
start_time = utime.localtime()[3]  # 获取开机时间作为饲料第一次储投喂时间
mqtt_object = ''  # mqtt服务器连接对象
# 本地时间字典
local_time_dic = {"1": ["00:00", "000", "on"],
                  "2": ["00:00", "000", "on"],
                  "3": ["00:00", "000", "on"],
                  "4": ["00:00", "000", "on"]
                  }
# 本地设置字典
local_setting_dic = {"empty_type": "true",  # 饲料不足提醒功能开关标志位默认开启为True
                     "timeout_type": "true",  # 饲料存储超时提醒功能开关标志位默认开启为True
                     "eat_type": "true",  # 宠物未进食提醒功能开关标志位默认开启为True
                     "bluetooth_type": "true"  # 蓝牙开关功能标志位默认开启为True
                     }
# 机器状态字典
local_state_dic = {"num": "4",  # 当前时间表执行状态标志位
                   "empty_bool": False,  # 饲料不足标志位默认饲料充足为False
                   "timeout_bool": False,  # 饲料存储超时标志位默认饲料存储不超时为False
                   "eat_bool": False,  # 宠物未进食标志位默认宠物已进食为False
                   # "time_value": utime.localtime()[0:3],  # 将开机时间作为第一次存储饲料时间
                   "food_value": [False, 00, 000]  # 是否投喂饲料 投喂饲料时间 投喂饲料重量
                   }
# 小程序显示数组
local_show_dic = {"food": "false",  # 当前是否处于投喂状态
                  "food_time": "00:00",  # 上次投喂饲料时间
                  "empty": "true",  # 当前饲料是否充足
                  "empty_time": [utime.localtime()[0], utime.localtime()[1], utime.localtime()[2]]   # 将开机时间作为第一次存储饲料时间
                  }

name = 'ESP32'  # 设备蓝牙名称

oled.oled_start()  # 显示开机界面

# 打开蓝牙获取WiFi信息
set_list = ['连接蓝牙', name, '配置网络', 2]  # 设置提醒界面显示的内容
oled.oled_set(set_list)  # 显示蓝牙连接提醒界面

bluetooth = blue.blue_connect(name)  # 连接蓝牙
msg = ''  # 初始化蓝牙接收到的数据为空
while not (blue.BLE_MSG == 'end'):  # 当接收到end表示WiFi信息接收完毕
    if (blue.BLE_MSG not in msg) and (blue.BLE_MSG != ''):
        msg = msg + blue.BLE_MSG  # 拼接WiFi信息
    else:
        pass

# msg = 'xiaomishouji;191543137'  # WiFi密码蓝牙接收测试
print(msg)
wifi_name = msg.split(' ')[0]  # 格式:wifi_name;wifi_pwd之间以";"作为分割
wifi_pwd = msg.split(' ')[1]

blue.BLE_MSG = ""  # 重置接收到的蓝牙信息
msg = ''  # 重置接收到的蓝牙信息

# 通过蓝牙配网ESP32-CAM


# 连接WiFi失败则继续捕获蓝牙数据
while not (wifi.do_connect(wifi_name, wifi_pwd, 10)):
    print('网络连接超时！请重新发送wifi数据')
    while not (blue.BLE_MSG == 'end'):
        if (blue.BLE_MSG not in msg) and (blue.BLE_MSG != ''):
            msg = msg + blue.BLE_MSG
        else:
            pass
    wifi_name = msg.split(';')[0]  # 格式:wifi_name;wifi_pwd之间以空格作为分割
    wifi_pwd = msg.split(';')[1]

    blue.BLE_MSG = ""  # 重置接收到的蓝牙信息
    msg = ''  # 重置接收到的蓝牙信息

top[1] = 'on'  # 状态栏显示数组中wifi连接标志位置为on

# 蓝牙获取数据结束显示主体页面
oled.oled_body(top, local_time_dic, local_state_dic['num'])


# 本地后台线程函数
def get_mqtt_dic(*args, **kwargs):
    global top
    global start_time
    global local_time_dic
    global local_setting_dic
    global local_state_dic
    global matt_object

    # 巴法服务器配置
    # config = ['bbccd1aa53cc4e6e945ad0340ba5c48d', 'bemfa.com', 9501]
    # 公共mqtt服务器连接配置
    # config = ['ESP32', 'broker-cn.emqx.io', 1883]
    # 公共mqtt服务器连接配置
    config = ['ESP32', '8.130.27.88', 1883]
    mqtt_object = mqtt.mqtt_connect(config[0], config[1], config[2])  # 连接mqtt服务器

    topic = ['time_dic', 'setting_dic', 'show_dic']  # mqtt服务器主题列表
    mqtt_dic = mqtt.get_msg(mqtt_object, topic)
    # 同步本地主题到服务器
    mqtt.send_msg(mqtt_object, 'time_dic', local_time_dic)
    mqtt.send_msg(mqtt_object, 'show_dic', local_show_dic)
    mqtt.send_msg(mqtt_object, 'setting_dic', local_setting_dic)

    # mqtt.send_msg(mqtt_object, 'time_dic', json.dumps(local_time_dic))
    # mqtt.send_msg(mqtt_object, 'setting_dic', json.dumps(local_setting_dic))
    # mqtt.send_msg(mqtt_object, 'show_dic', json.dumps(local_state_dic))

    while True:
        # 获取服务器主题 & 检查WiFi是否连接
        if wifi.wifi_link:
            top[1] = 'on'
            mqtt_dic = mqtt.get_msg(mqtt_object, topic)  # 获取mqtt服务器主题值
            print('mqtt_dic = ', mqtt_dic)
            local_time_dic = eval(mqtt_dic['time_dic'.encode()].decode('utf-8'))  # 保存服务器时间字典
            local_setting_dic = eval(mqtt_dic['setting_dic'.encode()].decode('utf-8'))  # 保存服务器设置字典
            local_show_dic = eval(mqtt_dic['show_dic'.encode()].decode('utf-8'))  # 保存服务器状态字典
            # local_state_dic = eval(mqtt_dic['state_dic'.encode()].decode('utf-8'))  # 保存服务器状态字典
        else:
            top[0] = 'off'

        time_data = utime.localtime()  # 获取本地时间
        weight_data = weigher.get_weight()  # 获取餐盘重量

        # 饲料不足提醒
        # local_setting_dic['empty_type'] == "true"  饲料不足提醒功能打开
        # not weigher2.is_full()  薄膜压力传感器检测饲料不足
        # not local_state_dic['empty_bool']  未曾发出饲料不足警报
        if local_setting_dic['empty_type'] == "true" and (not weigher2.is_full()) and (not local_state_dic['empty_bool']):
            # local_state_dic['empty_bool'] = True  # 警报设置为已发出
            # mqtt.send_msg(mqtt_object, 'state_dic', local_state_dic)  # 发布主题
            local_show_dic["empty"] = "false"  # 更改小程序显示当前饲料不足
            mqtt.send_msg(mqtt_object, 'show_dic', local_show_dic)  # 发布主题
            buzzer.buzzer_play()  # 蜂鸣器报警
            if weigher2.is_full():  # 饲料由空变为满则为存储饲料一次
                # local_state_dic['time_value'] = utime.localtime()[0:3]  # 记录存储饲料时间
                # mqtt.send_msg(mqtt_object, 'state_dic', local_state_dic)  # 发布主题
                # local_state_dic['empty_bool'] = False  # 警报设置为未曾发出过
                local_show_dic['empty_time'] = utime.localtime()[0:3]  # 更改小程序显示存储饲料时间im
                local_show_dic["empty"] = "true"  # 更改小程序显示当前饲料充足
                mqtt.send_msg(mqtt_object, 'show_dic', local_show_dic)  # 发布主题
                local_state_dic['timeout_bool'] = False  # 警报设置为未曾发出过
            else:
                pass
        else:
            pass

        # 存储饲料超时提醒
        last_time = local_state_dic['time_value']  # 获取上次存储饲料时间
        delta_time = (utime.localtime()[0] - last_time[0]) * 365 + (utime.localtime()[1] - last_time[1]) * 30 + (utime.localtime()[2] - last_time[2])  # 计算存储饲料时间差值
        # 时间差值大于14天 & 未曾发出警报 & 饲料存储超时提醒功能打开
        if (delta_time > 14) and (not local_state_dic['timeout_bool']) and local_setting_dic['timeout_type']:
            local_state_dic['timeout_bool'] = True  # 警报设置为发出过
            buzzer.buzzer_play()  # 蜂鸣器报警
            mqtt.send_msg(mqtt_object, 'state_dic', local_state_dic)  # 发布主题
        else:
            pass

        # 未进食提醒
        # 未进食提醒功能打开 & 当前时间和投喂饲料时间间隔一小时以上 & 剩余饲料重量在50g以上 & 未曾发出警报就发出未进食提醒
        if local_setting_dic['eat_type'] and ((utime.localtime()[3] - local_state_dic['food_value'][1]) > 1) and (weight_data > 50) and (not local_state_dic['eat_bool']):
            mp3.mp3_play('start')  # 再次发送语音呼唤宠物进食
            local_state_dic['eat_bool'] = True

        # 投喂饲料
        top[0] = str(time_data[3]) + ':' + str(time_data[4])  # 时间元组中提取出小时和分钟
        for each in local_time_dic.values():  # 提取本地时间字典中的所有值
            # 时间到达计划时间 & 餐盘重量小于计划投喂重量 & 未曾开始投喂
            if (top[0] == each[0]) and (weight_data < int(each[1])) and (not local_state_dic['food_value'][0]):
                local_state_dic['food_value'][0] = True  # 开始投喂饲料标志
                motor.main(180)  # 打开投料口
                mp3.mp3_play('start')  # 发送语音呼唤宠物进食
                local_state_dic['food_value'][2] = int(each[1])  # 记录投喂饲料重量
                mqtt.send_msg(mqtt_object, 'state_dic', local_state_dic)  # 发布主题
            # 餐盘重量大于计划投喂重量 & 已经开始投喂
            if (weight_data > int(local_state_dic['food_value'][2])) and (local_state_dic['food_value'][0]):
                local_state_dic['food_value'][0] = False  # 结束投喂饲料标志
                motor.main(0)  # 关闭投料口
                local_state_dic['food_value'][1] = utime.localtime()[3]  # 记录投喂饲料时间
                if (local_state_dic['num'] + 1) in local_setting_dic:
                    local_state_dic['num'] = local_state_dic['num'] + 1  # 投喂一次后将指向下一个投喂时间

                mqtt.send_msg(mqtt_object, 'state_dic', local_state_dic)  # 发布主题

        time.sleep(1)


# 按键扫描线程
# def scan(*args, **kwargs):
#     global key
#     while True:
#         key = keyboard.key_scan()


# 创建新线程获取mqtt数据&处理mqtt数据
thread_1 = _thread.start_new_thread(get_mqtt_dic, (1,))
# 创建新线程获取键盘输入
# thread_2 = _thread.start_new_thread(scan, (2,))

# 创建键盘对象
key = keyboard.Keyboard()

# 主界面循环
while True:
    oled.oled_body(top, local_time_dic, local_state_dic['num'])  # 显示主界面

    key_1 = 1  # 选中设置选项的位置
    out_1 = False  # 打开设置界面的标志
    if key.key_down == '*':  # 确认键按下进入设置界面
        out_1 = True
        key.key_down = ''  # 清空键盘捕获的值
    else:
        pass

    # 设置界面循环
    while out_1:
        out_2 = False  # 进入子设置界面的标志

        key_1_1 = 1
        time_1 = []
        weight_1 = []
        type_1 = 'on'

        key_1_2 = 1  # 选中设置选项的位置
        empty_type = '开'  # 默认项显示状态
        timeout_type = '开'
        eat_type = '开'

        key_1_3 = 1  # 选中设置选项的位置
        bluetooth_type = '开'  # 默认项显示状态

        set_list = ['投喂设置', '饲料设置', '无线设置', '关于本机', key_1]
        oled.oled_set(set_list)
        # 向下选择选项
        if key.key_down == 'B':
            if key_1 < 4:
                key_1 = key_1 + 1
            else:
                key_1 = 1
            key.key_down = ''  # 清空键盘捕获的值
        # 向上选择选项
        elif key.key_down == 'A':
            if key_1 > 1:
                key_1 = key_1 - 1
            else:
                key_1 = 4
            key.key_down = ''  # 清空键盘捕获的值
        # 退出设置界面
        elif key.key_down == '#':
            out_1 = False
            key.key_down = ''  # 清空键盘捕获的值
        # 进入设置子界面
        elif key.key_down == '*':
            out_2 = True
            key.key_down = ''  # 清空键盘捕获的值
        else:
            pass

        # 子设置界面循环
        while out_2:

            # 投喂设置界面
            if key_1 == 1:
                out_2_1 = False  # 进入添加时间子界面标志
                set_list_1 = ['添加', 1]
                oled.oled_set(set_list_1)
                # 退出到投喂设置界面
                if key.key_down == '#':
                    out_2 = False
                    key.key_down = ''  # 清空键盘捕获的值
                # 进入添加时间子界面
                elif key.key_down == '*':
                    out_2_1 = True
                    key.key_down = ''  # 清空键盘捕获的值
                '''
                #添加时间子界面循环
                while out_2_1:
                    # 向下选择选项
                    if key == 'B':
                        if key_1_1 < 4:
                            key_1_1 = key_1_1 + 1
                        else:
                            key_1_1 = 1
                    # 向上选择选项
                    elif key == 'A':
                        if key_1_1 > 1:
                            key_1_1 = key_1_1 - 1
                        else:
                            key_1_1 = 4
                    # 输入时间
                    elif key_1_1 == 2:
                        if key in ['0', '1', '2']:
                            time_1[1] = key


                    set_list = ['保存', '--:--', '---g', '--', key_1_1]
                    oled.oled_set(set_list)'''

            # 饲料设置界面
            elif key_1 == 2:
                set_list_2 = ['保存设置', '不足提醒：' + empty_type, '超时提醒：' + timeout_type,
                              '未进食提醒：' + eat_type, key_1_2]
                oled.oled_set(set_list_2)

                # 向下选择选项
                if key.key_down == 'B':
                    if key_1_2 < 4:
                        key_1_2 = key_1_2 + 1
                    else:
                        key_1_2 = 1
                    key.key_down = ''  # 清空键盘捕获的值
                # 向上选择选项
                elif key.key_down == 'A':
                    if key_1_2 > 1:
                        key_1_2 = key_1_2 - 1
                    else:
                        key_1_2 = 4
                    key.key_down = ''  # 清空键盘捕获的值
                # 修改设置
                elif key.key_down == '*':
                    # 设置不足提醒开关
                    if (key_1_2 == 2) and local_setting_dic['empty_type']:
                        empty_type = '关'
                    elif (key_1_2 == 2) and (not local_setting_dic['empty_type']):
                        empty_type = '开'
                    # 设置超时提醒开关
                    elif (key_1_2 == 3) and local_setting_dic['timeout_type']:
                        timeout_type = '关'
                    elif (key_1_2 == 3) and (not local_setting_dic['timeout_type']):
                        timeout_type = '开'
                    # 设置未进食提醒开关
                    if (key_1_2 == 4) and local_setting_dic['eat_type']:
                        eat_type = '关'
                    elif (key_1_2 == 4) and (not local_setting_dic['eat_type']):
                        eat_type = '开'
                    # 保存设置
                    elif key_1_2 == 1:
                        if empty_type == '开':
                            local_setting_dic['empty_type'] = True
                        else:
                            local_setting_dic['empty_type'] = False
                        if timeout_type == '开':
                            local_setting_dic['timeout_type'] = True
                        else:
                            local_setting_dic['timeout_type'] = False
                        if eat_type == '开':
                            local_setting_dic['eat_type'] = True
                        else:
                            local_setting_dic['eat_type'] = False

                        mqtt.send_msg(mqtt_object, 'setting_dic', local_setting_dic)  # 发布主题
                    key.key_down = ''  # 清空键盘捕获的值
                # 退出饲料设置界面
                elif key.key_down == '#':
                    out_2 = False
                    key.key_down = ''  # 清空键盘捕获的值
                else:
                    pass

            # 无线设置界面
            elif key_1 == 3:
                set_list_3 = ['保存设置', '蓝牙：' + bluetooth_type, '小程序二维码', 'wifi:' + wifi_name, key_1_3]
                oled.oled_set(set_list_3)
                print("test")

                # 向下选择选项
                if key.key_down == 'B':
                    if key_1_3 < 4:
                        key_1_3 = key_1_3 + 1
                    else:
                        key_1_3 = 1
                    key.key_down = ''  # 清空键盘捕获的值
                # 向上选择选项
                elif key.key_down == 'A':
                    if key_1_3 > 1:
                        key_1_3 = key_1_3 - 1
                    else:
                        key_1_3 = 4
                    key.key_down = ''  # 清空键盘捕获的值
                # 改变选项的值
                elif key.key_down == '*':
                    # 改变蓝牙连接状态
                    if (key_1_3 == 2) and local_setting_dic['bluetooth_type']:
                        bluetooth_type = '关'
                        try:
                            del bluetooth  # 销毁蓝牙对象关闭蓝牙
                        except:
                            pass
                    elif (key_1_3 == 2) and (not local_setting_dic['bluetooth_type']):
                        bluetooth_type = '开'
                        bluetooth = blue.blue_connect(name)  # 初始化蓝牙对象打开蓝牙
                    # 显示小程序二维码
                    elif key_1_3 == 3:
                        pass
                    # 保存设置
                    elif key_1_3 == 1:
                        if bluetooth_type == '开':
                            local_setting_dic['bluetooth_type'] = True
                        else:
                            local_setting_dic['bluetooth_type'] = False
                        mqtt.send_msg(mqtt_object, 'setting_dic', local_setting_dic)  # 发布主题
                    key.key_down = ''  # 清空键盘捕获的值
                # 退出无线设置界面
                elif key.key_down == '#':
                    out_2 = False
                    key.key_down = ''  # 清空键盘捕获的值
                else:
                    pass

            # 关于本机界面
            elif key_1 == 4:
                set_list_4 = ['宠物自动喂食器', '指导老师：李强', '学生：汤玉杰', '2023-1-10 V1.0', 1]
                oled.oled_set(set_list_4)

                # 退出关于本机界面
                if key.key_down == '#':
                    out_2 = False
                    key.key_down = ''  # 清空键盘捕获的值

            else:
                pass
