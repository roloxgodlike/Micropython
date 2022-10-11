import time
import math
from machine import SPI, SDCard
from fpioa_manager import fm
from Maix import GPIO

LOGGER_ENABLE = 0
_spi_baudrate = 3 * 1000 * 1000
_spi_cs = 0
_spi1 = 0


def SPI_Flash_Init():
    global _spi1, _spi_cs
    fm.register(17, fm.fpioa.GPIOHS10, force=True)  # cs
    _spi_cs = GPIO(GPIO.GPIOHS10, GPIO.OUT)

    _spi1 = SPI(
        # SPI ID， 取值范围[0,4]， 目前只支持 0 和 1 、4 ， 并且只能是主机模式， 2 只能作为从机，目前未实现， 3 保留, 4 使用软模拟 SPI（.SPI_SOFT）
        1,
        # SPI 模式， MODE_MASTER 或者MODE_MASTER_2或者MODE_MASTER_4或者MODE_MASTER_8或者MODE_SLAVE， 目前只支持MODE_MASTER
        mode=SPI.MODE_MASTER,
        baudrate=_spi_baudrate,
        polarity=1,  # 极性， 取值为 0 或 1， 表示 SPI 在空闲时的极性， 0 代表低电平， 1 代表高电平
        phase=1,  # 相， 取值位 0 或 1， 表示在时钟的第一个还是第二个跳变沿采集数据， 0 表示第一个， 1 表示第二个
        bits=8,  # 数据宽度， 默认值为8， 取值范围[4,32]
        firstbit=SPI.MSB,  # 目前只能是SPI.MSB，代表传输时高位在前。
        #  cs0=16, sck=18, mosi=19, miso=20,
        sck=33, mosi=34, miso=35,
        # crc=0x7
    )


def SPI_Flash_Deinit():
    if _spi1:
        _spi1.deinit()

# define W25X_WriteEnable       0x06
# define W25X_WriteDisable      0x04
# define W25X_ReadStatusReg     0x05
# define W25X_WriteStatusReg    0x01
# define W25X_ReadData          0x03
# define W25X_FastReadData      0x0B
# define W25X_FastReadDual      0x3B
# define W25X_PageProgram       0x02
# define W25X_BlockErase        0xD8
# define W25X_SectorErase       0x20
# define W25X_ChipErase         0xC7
# define W25X_PowerDown         0xB9
# define W25X_ReleasePowerDown  0xAB
# define W25X_DeviceID          0xAB
# define W25X_ManufactDeviceID  0x90
# define W25X_JedecDeviceID     0x9F


def SPI_Flash_ReadID():
    ret = bytearray(2)
    _spi_cs.value(0)
    _spi1.write(b'\x90\x00\x00\x00\x00')
    _spi1.write_readinto(b'\xFF\xFF', ret)
    _spi_cs.value(1)
    print('>>>SPI_Flash_ReadID:', ret)
    if (ret[0] != 0x16):
        print('>>>Flash not support!')
        return False
    print('>>>Flash ID ok!')
    return True


def SPI_Flash_Read_SR():
    # //读取SPI_FLASH的状态寄存器
    # //BIT7  6   5   4   3   2   1   0
    # //SPR   RV  TB BP2 BP1 BP0 WEL BUSY
    # //SPR:默认0,状态寄存器保护位,配合WP使用
    # //TB,BP2,BP1,BP0:FLASH区域写保护设置
    # //WEL:写使能锁定
    # //BUSY:忙标记位(1,忙;0,空闲)
    # //默认:0x00
    ret = bytearray(1)
    _spi_cs.value(0)
    _spi1.write(0x05)
    _spi1.write_readinto(b'\xFF', ret)
    _spi_cs.value(1)

    sr = ret[0]
    # if LOGGER_ENABLE:
    # print('Read SR:', sr)
    return sr


def SPI_FLASH_Write_SR():
    # //写SPI_FLASH状态寄存器
    # //只有SPR, TB, BP2, BP1, BP0(bit 7, 5, 4, 3, 2)可以写!!!
    _spi_cs.value(0)
    _spi1.write(0x01)
    _spi_cs.value(1)
    if LOGGER_ENABLE:
        print('>>>SPI_FLASH_Write_SR')


def SPI_FLASH_Write_Enable():
    # //SPI_FLASH写使能
    # //将WEL置位
    ret = bytearray(1)
    _spi_cs.value(0)
    _spi1.write(0x06)  # 发送写使能
    _spi_cs.value(1)
    if LOGGER_ENABLE:
        print('>>>SPI_FLASH_Write_Enable')


def SPI_Flash_Read(pBuffer, ReadAddr, NumByteToRead):
    # //读取SPI FLASH
    # //在指定地址开始读取指定长度的数据
    # //pBuffer: 数据存储区
    # //ReadAddr: 开始读取的地址(24bit)
    # //NumByteToRead: 要读取的字节数(最大65535)
    # ret = bytearray(NumByteToRead)
    tmp = bytearray(1)
    _spi_cs.value(0)
    _spi1.write(0x03)  # 发送读取命令
    _spi1.write((ReadAddr >> 16) & 0xFF)
    _spi1.write((ReadAddr >> 8) & 0xFF)
    _spi1.write((ReadAddr) & 0xFF)

    # tmp = bytearray(NumByteToRead) #快但是不可靠
    # for i in range(NumByteToRead):
    #     tmp[i] = 0xFF
    # _spi1.write_readinto(tmp, pBuffer)
    for i in range(NumByteToRead):
        _spi1.write_readinto(b'\xFF', tmp)
        pBuffer[i] = tmp[0]

    _spi_cs.value(1)
    if LOGGER_ENABLE:
        print('>>>SPI_Flash_Read:', pBuffer)


def SPI_Flash_Erase_Chip():
    # //擦除整个芯片
    # //整片擦除时间:
    # //W25X16:25s
    # //W25X32:40s
    # //W25X64:40s
    # //等待时间超长...
    SPI_FLASH_Write_Enable()  # SET WEL
    SPI_Flash_Wait_Busy()
    _spi_cs.value(0)
    _spi1.write(0xC7)  # 发送片擦除命令 0xC7
    _spi_cs.value(1)
    SPI_Flash_Wait_Busy()
    print('>>>SPI_Flash_Erase_Chip')


def SPI_Flash_Erase_Sector(EraseAddr):
    # //擦除一个扇区
    # //EraseAddr:扇区地址 0~511 for w25x16
    # //擦除一个扇区的最少时间:150ms
    # _EraseAddr = EraseAddr * 4096 #不清楚原因
    SPI_FLASH_Write_Enable()  # //SET WEL
    SPI_Flash_Wait_Busy()
    _spi_cs.value(0)
    _spi1.write(0x20)  # 发送扇区擦除指令
    _spi1.write((EraseAddr >> 16) & 0xFF)  # 发送24bit地址
    _spi1.write((EraseAddr >> 8) & 0xFF)
    _spi1.write((EraseAddr) & 0xFF)
    _spi_cs.value(1)
    SPI_Flash_Wait_Busy()  # 等待擦除完成
    print('>>>SPI_Flash_Erase_Sector: 0x%06X' % (EraseAddr))


def SPI_Flash_Wait_Busy():
    # 等待BUSY位清空
    ret = SPI_Flash_Read_SR()
    while (ret & 0x01):
        ret = SPI_Flash_Read_SR()


def SPI_Flash_Write_Page(pBuffer, WriteAddr, NumByteToWrite):
    # //SPI在一页(0~65535)内写入少于256个字节的数据
    # //在指定地址开始写入最大256字节的数据
    # //pBuffer:数据存储区
    # //WriteAddr:开始写入的地址(24bit)
    # //NumByteToWrite:要写入的字节数(最大256),该数不应该超过该页的剩余字节数!!!
    if (NumByteToWrite <= 0):
        return

    SPI_FLASH_Write_Enable()  # SET WEL

    _spi_cs.value(0)
    _spi1.write(0x02)  # 发送写页命令
    _spi1.write((WriteAddr >> 16) & 0xFF)
    _spi1.write((WriteAddr >> 8) & 0xFF)
    _spi1.write((WriteAddr) & 0xFF)
    _spi1.write(pBuffer)
    _spi_cs.value(1)

    SPI_Flash_Wait_Busy()  # 等待写入结束
    if LOGGER_ENABLE:
        print('>>>SPI_Flash_Write_Page: 0x%06X %dBytes' %
              (WriteAddr, NumByteToWrite))


def SPI_Flash_Write_NoCheck(pBuffer, WriteAddr, NumByteToWrite):
    # //无检验写SPI FLASH
    # //必须确保所写的地址范围内的数据全部为0XFF,否则在非0XFF处写入的数据将失败!
    # //具有自动换页功能
    # //在指定地址开始写入指定长度的数据,但是要确保地址不越界!
    # //pBuffer:数据存储区
    # //WriteAddr:开始写入的地址(24bit)
    # //NumByteToWrite:要写入的字节数(最大65535)
    # //CHECK OK
    _WriteAddr = WriteAddr
    _NumByteToWrite = 0
    _buffIdx = 0
    _is_empty = 1  # 过滤全0xFF的数据, 如果一页全是0xFF则无需写入

    # 不足或刚好一页直接写
    if (NumByteToWrite <= 256):
        for i in range(NumByteToWrite):
            if (pBuffer[i] != 0xFF):
                _is_empty = 0
        if not _is_empty:
            SPI_Flash_Write_Page(pBuffer, WriteAddr, NumByteToWrite)
        else:
            print('page empty, addr:0x%06X, bIdx:%d' % (_WriteAddr, _buffIdx))
        return

    # 大于一页分次写
    total_cnt = math.ceil(NumByteToWrite / 256)  # 写的次数
    for idx in range(total_cnt):
        if (idx != (total_cnt - 1)):
            _NumByteToWrite = 256
        else:
            if (NumByteToWrite % 256 == 0):
                _NumByteToWrite = 256
            else:
                _NumByteToWrite = NumByteToWrite % 256

        if LOGGER_ENABLE:
            print('total_cnt:', total_cnt, 'idx:', idx, 'num:',
                  _NumByteToWrite, 'addr: 0x%06X' % (_WriteAddr))

        _is_empty = 1
        _pBuffer = bytearray(_NumByteToWrite)
        for i in range(_NumByteToWrite):
            if (_is_empty and pBuffer[_buffIdx] != 0xFF):
                _is_empty = 0
            _pBuffer[i] = pBuffer[_buffIdx]
            _buffIdx += 1  # 写入字节每次偏移

        if not _is_empty:
            SPI_Flash_Write_Page(_pBuffer, _WriteAddr, _NumByteToWrite)
            if LOGGER_ENABLE:
                print('after write page, addr: 0x%06X' %
                      (_WriteAddr), 'buffIdx: ', _buffIdx)
        else:
            if LOGGER_ENABLE:
                print('page empty, addr:0x%06X, bIdx:%d' %
                      (_WriteAddr, _buffIdx))

        _WriteAddr += _NumByteToWrite  # 写入起始地址每次按上次写入数偏移


if __name__ == '__main__':
    page_size = 32
    # test_size = 8388608
    test_size = 10 * page_size
    test_addr = 0x000000

    start_time = time.time()
    rBuffer = bytearray(page_size)
    wBuffer = bytearray(test_size)

    time.sleep(1)
    SPI_Flash_Init()
    time.sleep(1)

    while not SPI_Flash_ReadID():
        print('...W25Q64 not ready...')
        time.sleep_ms(1000)

    SPI_Flash_Erase_Chip()
    # SPI_Flash_Read_SR()
    # SPI_FLASH_Write_SR()
    # SPI_FLASH_Write_Enable()
    # SPI_Flash_Read(rBuffer, test_addr, test_size)

    for i in range(test_size):
        wBuffer[i] = i & 0xFF
        # wBuffer[i] = 0xFF

    # SPI_Flash_Write_Page(wBuffer, test_addr, test_size)
    SPI_Flash_Write_NoCheck(wBuffer, test_addr, test_size)
    # SPI_Flash_Read(rBuffer, test_addr, test_size)
    # SPI_Flash_Erase_Sector(test_addr)
    # SPI_Flash_Read(rBuffer, test_addr, test_size)

    cnt = math.ceil(test_size / page_size)
    print('cnt', cnt)
    for i in range(cnt):
        SPI_Flash_Read(rBuffer, test_addr, page_size)
        # print('\n----', i, test_addr, rBuffer)
        test_addr += page_size
        # time.sleep_ms(1000)

    time.sleep(1)
    SPI_Flash_Deinit()
    # SPI_Flash_ReadID() #exception
    print('\n-----time use', (time.time() - start_time), 's-----')

    SDCard.remount()
    time.sleep(1)
