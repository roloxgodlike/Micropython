import time
from machine import UART
from fpioa_manager import fm

#映射串口引脚
fm.register(6, fm.fpioa.UART1_RX, force=True)
fm.register(7, fm.fpioa.UART1_TX, force=True)
fm.register(10, fm.fpioa.UART2_RX, force=True)# x11-io10 RX x12-io11 TX
fm.register(11, fm.fpioa.UART2_TX, force=True)

#初始化串口
# uart = UART(UART.UART1,
# baudrate=2400,
# bits=8,
# parity=UART.PARITY_EVEN,
# stop=0,
# timeout=1000,
# read_buf_len=1024)

uart485 = UART(UART.UART2,
baudrate=2400,
bits=8,
parity=UART.PARITY_EVEN,
stop=0,
timeout=100,
read_buf_len=512)

def BytesToHexStr(_bytes):
    return ''.join(["%02X " % b for b in _bytes]).strip()

# print(text.decode('utf-8')) #REPL打印
# uart.write('I got'+text.decode('utf-8')) #数据回传
CONST_CMD_ADDR = b'\x68\xAA\xAA\xAA\xAA\xAA\xAA\x68\x13\x00\xDF\x16'
while True:
    uart485.write(CONST_CMD_ADDR)
    time.sleep(1)
    _bytes = uart485.read() #读取数据
    if _bytes: #如果读取到了数据
        print('UART-Rx-len:', len(_bytes), 'hex:', BytesToHexStr(_bytes))
        time.sleep(1)

