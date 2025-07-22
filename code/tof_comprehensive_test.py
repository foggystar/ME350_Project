# -*- coding: utf-8 -*-
import serial
import time
import binascii

print("TOF模块全面测试工具")
print("="*50)

# 树莓派串口列表
possible_ports = ['/dev/serial0', '/dev/ttyAMA0', '/dev/ttyS0']
serial_connection = None

# 尝试连接串口
for port in possible_ports:
    try:
        print(f"尝试连接 {port}...")
        serial_connection = serial.Serial(port, 9600, timeout=2)
        if serial_connection.isOpen():
            print(f"✓ {port} 连接成功!")
            break
    except Exception as e:
        print(f"✗ {port} 连接失败: {e}")

if not serial_connection or not serial_connection.isOpen():
    print("所有串口连接失败！")
    exit(1)

def test_different_baudrates():
    """测试不同波特率"""
    baudrates = [9600, 115200, 57600, 38400, 19200, 4800]
    
    for baud in baudrates:
        try:
            print(f"\n测试波特率: {baud}")
            if serial_connection.isOpen():
                serial_connection.close()
            
            serial_connection.baudrate = baud
            serial_connection.open()
            
            # 等待数据
            for i in range(5):
                if serial_connection.inWaiting() > 0:
                    data = serial_connection.read(serial_connection.inWaiting())
                    print(f"波特率 {baud} 接收到数据: {binascii.hexlify(data)}")
                    return baud
                time.sleep(0.2)
                
        except Exception as e:
            print(f"波特率 {baud} 测试失败: {e}")
    
    return 9600  # 默认返回9600

def send_common_commands():
    """发送常见的TOF模块命令"""
    commands = [
        b'\x55',  # 常见的启动命令
        b'\x01',  # 测距命令
        b'\x02',  # 连续测距
        b'\x55\xAA',  # 组合命令
        b'\x57\x00\x00\x00\x00\x00\x00\x00\x57',  # TOF200/400系列命令
        b'\x55\x01\x01\x57',  # 另一种常见格式
    ]
    
    print("\n发送常见命令测试:")
    for i, cmd in enumerate(commands):
        print(f"发送命令 {i+1}: {binascii.hexlify(cmd)}")
        try:
            serial_connection.write(cmd)
            time.sleep(0.5)  # 等待响应
            
            if serial_connection.inWaiting() > 0:
                response = serial_connection.read(serial_connection.inWaiting())
                print(f"  响应: {binascii.hexlify(response)}")
                return True
            else:
                print("  无响应")
        except Exception as e:
            print(f"  发送失败: {e}")
    
    return False

def passive_listening_test():
    """被动监听测试"""
    print("\n被动监听测试 (30秒)...")
    print("请确保TOF模块已通电并且在测距范围内有目标物体")
    
    start_time = time.time()
    data_received = False
    
    while time.time() - start_time < 30:
        if serial_connection.inWaiting() > 0:
            data = serial_connection.read(serial_connection.inWaiting())
            print(f"接收到数据: {binascii.hexlify(data)}")
            print(f"数据长度: {len(data)} 字节")
            print(f"ASCII表示: {data}")
            data_received = True
            
            # 尝试解析
            if len(data) >= 4:
                try_parse_distance(data)
            
        time.sleep(0.1)
        if int(time.time() - start_time) % 5 == 0:
            print(".", end="", flush=True)
    
    return data_received

def try_parse_distance(raw_data):
    """尝试解析距离数据"""
    print(f"\n尝试解析距离数据:")
    hex_str = binascii.hexlify(raw_data).decode()
    print(f"十六进制字符串: {hex_str}")
    
    # 方法1: 假设距离在第3-4字节（大端序）
    if len(raw_data) >= 4:
        dist1 = (raw_data[2] << 8) | raw_data[3]
        print(f"方法1 (字节2-3): {dist1} mm")
    
    # 方法2: 假设距离在第1-2字节（大端序）
    if len(raw_data) >= 2:
        dist2 = (raw_data[0] << 8) | raw_data[1]
        print(f"方法2 (字节0-1): {dist2} mm")
    
    # 方法3: 小端序
    if len(raw_data) >= 4:
        dist3 = (raw_data[3] << 8) | raw_data[2]
        print(f"方法3 (字节2-3小端): {dist3} mm")

def main():
    print("\n开始全面测试...")
    
    # 1. 测试不同波特率
    optimal_baud = test_different_baudrates()
    print(f"\n使用波特率: {optimal_baud}")
    
    # 2. 发送命令测试
    cmd_success = send_common_commands()
    
    # 3. 被动监听
    if not cmd_success:
        print("\n命令测试未收到响应，开始被动监听...")
        passive_listening_test()
    
    print("\n测试完成!")
    print("\n故障排除建议:")
    print("1. 检查硬件连接:")
    print("   - TOF模块 VCC → 树莓派 5V/3.3V")
    print("   - TOF模块 GND → 树莓派 GND")
    print("   - TOF模块 TX → 树莓派 GPIO15 (RX)")
    print("   - TOF模块 RX → 树莓派 GPIO14 (TX)")
    print("2. 检查TOF模块供电指示灯")
    print("3. 查看TOF模块型号和说明书")
    print("4. 确认串口配置正确")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户中断")
    finally:
        if serial_connection and serial_connection.isOpen():
            serial_connection.close()
            print("串口已关闭")
