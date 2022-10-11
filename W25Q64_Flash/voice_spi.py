import time
import os
from machine import SDCard
from module_gpio import *
from module_spi import *
from module_file import *

_gpio_ = ClassGPIO()

file_path = '/sd/ReceivedTofile.bin'  # 8388608字节
file_read_size = 48 * 1024 #单次读取字节
file_download_flag = 0


def key_test_cb(KEY):
    global file_download_flag

    time.sleep_ms(10)
    if (KEY.value() == 1):
        return

    print("key down", KEY.value())
    if (file_download_flag != 0):
        print('>>>BUSY downloading!')
        return

    file_download_flag = 1


def error_handle():
    global file_download_flag

    _gpio_.led_rgb_red()
    file_download_flag = 0


def check_spi_flash_before_write():
    SPI_Flash_Init()
    # time.sleep_ms(1)
    ret = SPI_Flash_ReadID()
    if not ret:
        return False
    print('...start erase chip...')
    SPI_Flash_Erase_Chip()
    SPI_Flash_Deinit()
    return True


def file_read_and_write():
    global file_download_flag

    if (file_download_flag != 1):
        return

    file_download_flag = 2
    _gpio_.led_rgb_blue()
    time_start = time.time()
    print('...file_read_and_write', file_download_flag)

    if not check_spi_flash_before_write():
        error_handle()
        return
    print('...use time %.0fs...' % (time.time() - time_start))

    SDCard.remount()  # 必须再加载回sdcard否则烧写固件读不到
    time.sleep_ms(50)

    _file = 0
    _total_bytes_len = 0
    _read_page_idx = 0
    _read_bytes_len = 0
    _read_bytes_tmp = 0
    _seek_idx = 0

    try:

        _file = open(file_path, 'rb')
        # _file.seek(_seek_idx, 0)
        _read_bytes = _file.read(file_read_size)
        _seek_idx = _file.tell()

        while _read_bytes:

            _is_empty = 1
            _read_bytes_len = len(_read_bytes)

            #先拷贝出数据, 过滤全0xFF的数据
            _read_bytes_tmp = bytearray(_read_bytes_len)
            for i in range(_read_bytes_len):
                if (_is_empty and _read_bytes[i] != 0xFF):
                    _is_empty = 0
                _read_bytes_tmp[i] = _read_bytes[i]

            if (_read_page_idx % 5 == 0):
                print('...page: %d, readSize: %d, writeSize(seekIdx): %d'
                    % (_read_page_idx, _read_bytes_len, _total_bytes_len))

            if not _is_empty:
                _file.close()  # 释放文件句柄

                SPI_Flash_Init()  # 切换SPI并烧写
                # time.sleep_ms(1)
                SPI_Flash_Write_NoCheck(
                    _read_bytes_tmp, _total_bytes_len, _read_bytes_len)
                SPI_Flash_Deinit()

                SDCard.remount()  # 切换SPI再次打开文件
                time.sleep_ms(20)
                _file = open(file_path, 'rb')
            # else:
                # print('...page data empyt...', _read_page_idx)

            _read_page_idx += 1
            _total_bytes_len += _read_bytes_len

            _file.seek(_seek_idx, 0)
            _read_bytes = _file.read(file_read_size)
            _seek_idx = _file.tell()

    except Exception as e:
        print('...FILE ERROR!!!...', e)
        error_handle()
        return
    finally:
        if _file:
            _file.close()
            print('...read done', _read_page_idx, _total_bytes_len)

    if (_total_bytes_len == 0):
        error_handle()
        return

    print('...use time %.0fs...' % (time.time() - time_start))
    _gpio_.led_rgb_green()
    file_download_flag = 0


if __name__ == '__main__':
    SDCard.remount()
    _gpio_.init_led()
    _gpio_.led_rgb_red()

    while not len(os.listdir('/sd/')):
        print('...SD not ready...')
        time.sleep_ms(1000)
    print(os.listdir('/sd/'))
    time.sleep_ms(100)

    SPI_Flash_Init()
    while not SPI_Flash_ReadID():
        print('...W25Q64 not ready...')
        time.sleep_ms(1000)

    print('---init done---')
    _gpio_.led_rgb_all()
    _gpio_.init_key(key_test_cb)

    while 1:
        file_read_and_write()
        time.sleep_ms(100)
