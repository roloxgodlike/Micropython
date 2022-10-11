import os, time


# 字节bytes转化kb\m\g
def File_FormatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print('传入的字节格式不对')
        return 'Error'

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return '%fG' % (G)
        else:
            return '%fM' % (M)
    else:
        return '%fkb' % (kb)


# 获取文件大小
def File_GetFileSize(path):
    try:
        size = os.path.getsize(path)
        # return File_FormatSize(size)
        return size
    except Exception as err:
        print(err)


# 获取文件夹大小
def File_GetFolderSize(path):
    sumsize = 0
    try:
        filename = os.walk(path)
        for root, dirs, files in filename:
            for fle in files:
                size = os.path.getsize(path + fle)
                sumsize += size
        # return File_FormatSize(sumsize)
        return sumsize
    except Exception as err:
        print(err)

if __name__ == "__main__":

    # file_path = 'C:/Users/Administrator/Desktop/ReceivedTofile.bin'
    # folder_path = 'D:/work/MicroPython/workspace/W25Q64_Flash/'
    file_path = '/sd/ReceivedTofile.bin' #8388608字节
    # folder_path = '/sd/voice/'
    # print(File_GetFileSize(file_path))
    # print(File_GetFolderSize(folder_path))

    time.sleep(1)
    print(os.listdir('/sd/'))

    _total_page = 0
    _total_size = 0
    _file = 0
    try:
        _file = open(file_path, 'rb')
        bytes = _file.read(512)
        while bytes:
            _total_page += 1
            _total_size += len(bytes)
            print('>>>read page:', _total_page, len(bytes))
            bytes = _file.read(512)
    except Exception:
        print('>>>FILE ERROR!!!')
    finally:
        if _file:
            _file.close()
            print('>>>read done:', _total_page, _total_size)
