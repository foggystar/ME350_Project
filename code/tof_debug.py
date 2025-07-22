# -*- coding: utf-8 -*-
import serial
import time
import binascii

# 尝试多个可能的串口
possible_ports = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']
serial1 = None

print("正在尝试连接串口...")
for port in possible_ports:
    try:
        serial1 = serial.Serial(port, 9600, timeout=1)
        if serial1.isOpen():
            print(f"串口 {port} 连接成功")
            break
    except Exception as e:
        print(f"串口 {port} 连接失败: {e}")
        continue

if serial1 is None or not serial1.isOpen():
    print("所有串口连接失败，请检查设备连接")
    exit(1)

def hex_char_to_int(char):
    """将十六进制字符转换为整数"""
    if char >= '0' and char <= '9':
        return int(char)
    elif char >= 'a' and char <= 'f':
        return ord(char) - ord('a') + 10
    elif char >= 'A' and char <= 'F':
        return ord(char) - ord('A') + 10
    else:
        return 0

def parse_distance_data(data_str):
    """解析距离数据"""
    try:
        # 移除 b' 前缀和 ' 后缀（如果存在）
        if data_str.startswith("b'") and data_str.endswith("'"):
            data_str = data_str[2:-1]
        
        print(f"原始数据: {data_str}, 长度: {len(data_str)}")
        
        if len(data_str) < 10:
            print("数据长度不足")
            return None
            
        # 提取距离数据的4个字节（通常在固定位置）
        dat1 = data_str[6:7] if len(data_str) > 6 else '0'
        dat2 = data_str[7:8] if len(data_str) > 7 else '0'
        dat3 = data_str[8:9] if len(data_str) > 8 else '0'
        dat4 = data_str[9:10] if len(data_str) > 9 else '0'
        
        print(f"提取的数据位: {dat1}, {dat2}, {dat3}, {dat4}")
        
        # 转换为十六进制值
        val1 = hex_char_to_int(dat1)
        val2 = hex_char_to_int(dat2)
        val3 = hex_char_to_int(dat3)
        val4 = hex_char_to_int(dat4)
        
        print(f"转换的十六进制值: {val1}, {val2}, {val3}, {val4}")
        
        # 计算距离（毫米）
        distance = ((val1 * 16 + val2) * 256) + (val3 * 16 + val4)
        return distance
        
    except Exception as e:
        print(f"数据解析错误: {e}")
        return None

def main():
    global serial1
    time.sleep(0.1)
    
    # 检查是否有数据可读
    num = serial1.inWaiting()
    
    if num > 0:
        print(f"接收到 {num} 字节数据")
        try:
            # 读取原始数据
            raw_data = serial1.read(num)
            print(f"原始字节数据: {raw_data}")
            
            # 转换为十六进制字符串
            hex_data = str(binascii.b2a_hex(raw_data))
            print(f"十六进制数据: {hex_data}")
            
            # 解析距离
            distance = parse_distance_data(hex_data)
            if distance is not None:
                print(f"测量距离: {distance} mm ({distance/10:.1f} cm)")
            else:
                print("无法解析距离数据")
                
        except Exception as e:
            print(f"数据处理错误: {e}")
    else:
        print(".", end="", flush=True)  # 显示程序在运行

print("开始测距，按Ctrl+C退出...")
try:
    while True:
        main()
        time.sleep(0.5)  # 增加延时，便于观察
except KeyboardInterrupt:
    print("\n程序退出")
    if serial1 and serial1.isOpen():
        serial1.close()
