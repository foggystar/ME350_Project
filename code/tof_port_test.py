# -*- coding: utf-8 -*-
import serial
import time
import binascii

print("TOF测距模块调试工具")
print("="*50)

# 尝试连接不同的串口
ports_to_try = ['/dev/ttyUSB0', '/dev/ttyUSB1', '/dev/ttyACM0', '/dev/ttyACM1']

for port in ports_to_try:
    try:
        print(f"尝试连接 {port}...")
        ser = serial.Serial(port, 9600, timeout=2)
        if ser.isOpen():
            print(f"✓ {port} 连接成功!")
            
            # 测试数据接收
            print("等待数据...")
            for i in range(10):  # 尝试10次
                if ser.inWaiting() > 0:
                    data = ser.read(ser.inWaiting())
                    print(f"接收到数据: {data}")
                    print(f"十六进制: {binascii.hexlify(data)}")
                    print(f"长度: {len(data)} 字节")
                    break
                time.sleep(0.5)
                print(".", end="", flush=True)
            else:
                print(f"\n在 {port} 上没有接收到数据")
            
            ser.close()
            break
    except Exception as e:
        print(f"✗ {port} 连接失败: {e}")

print("\n检查清单:")
print("1. 确认TOF模块已正确连接到串口")
print("2. 检查波特率设置（通常为9600）")
print("3. 确认模块供电正常")
print("4. 检查串口设备文件权限")
print("5. 尝试不同的串口号")
