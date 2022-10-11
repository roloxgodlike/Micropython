import contextlib
from urllib.request import urlopen


def main():
    # with contextlib.closing(urlopen("http://www.baidu.com/")) as front_page:
    #     for line in front_page:
    #         print(line)

    a, b = 1+2j, 2+3j
    c, d = 31.2, 23.2
    print(a + b)
    print(a - b)
    print(a * b)
    print(a / b)
    print(c // d)
    print(c / d)
    print(2 ** 3)
    print(type(a), type(b), type(c), type(d))
    print('{}---{}'.format(a, b))
    print('%s---%.3f' % (c, d))
    print(isinstance(a, complex))
    print(isinstance(c, float))
    print(issubclass(bool, int))
    print('test\ntest2\\')
    print(r'test\ntest2\\')
    print('11111111111111\
222222222222\
333333333333')

    # a = set('abracadabra')
    # b = set('alacazam')
    # print(a)
    # print(a - b)     # a 和 b 的差集
    # print(a | b)     # a 和 b 的并集
    # print(a & b)     # a 和 b 的交集
    # print(a ^ b)     # a 和 b 中不同时存在的元素

    aaa = {x: x**2 for x in (2, 4, 6)}
    print(aaa)


class TestTopClass():

    def process(self, a, b):
        self._a = a
        self._b = b
        return self._a + self._b


class TestClass(TestTopClass):

    CONST_ATTR1 = 1
    CONST_ATTR2 = '2'
    CONST_ATTR3 = [1, 2, 3]

    def __enter__(self):
        print('__enter__')
        return self

    def __init__(self, a, b):
        self._a = a
        self._b = b

    # def process(self, a, b):
    #     self._a = a
    #     self._b = b
    #     return self._a - self._b

    def __exit__(self, exc_type, exc_value, traceback):
        print('__exit__')
        print(f'exc_type:{exc_type}')
        print(f'exc_value:{exc_value}')
        print(f'traceback:{traceback}')
        return True


if __name__ == '__main__':
    # main()
    # print(TestClass.CONST_ATTR1, TestClass.CONST_ATTR2, TestClass.CONST_ATTR3)
    # test_class = TestClass(1, 2)
    # print(isinstance(test_class, TestTopClass),
    #         isinstance(test_class, TestClass),
    #         issubclass(TestClass, TestTopClass))
    # print(test_class._a, test_class._b)
    # print(test_class.process(1, 2))
    # with TestClass(3, 4) as test_class:
    #     print(test_class._a, test_class._b)
    #     print(test_class.process(5, 6))
    # del test_class
    # print('done')

    bytes = b'\x31\x32'
    #bytes转hex字符串
    print(type(bytes), len(bytes), bytes, bytes[0], '0x' + format(bytes[0], '04X')) 
    str = ''.join(['%02X' % b for b in bytes]).strip()
    print(str)
    _hex = bytes.hex(':')
    print(_hex)
    #bytes转list
    bytelist = list(bytes)
    print(type(bytelist), bytelist, bytelist[0])
    #bytes转int
    _int = int.from_bytes(bytes, byteorder='big', signed=False)
    print(_int)
    #int转bytes
    _bytes = _int.to_bytes(3, byteorder='big', signed=False)
    print(_bytes, bytes == _bytes)
    #hex字符串转Ascii对应的bytes
    _hex_str = '31 32 33 34'
    print(bytes.fromhex(_hex_str))
    #格式化bytes
    print(b'\x68%b\x68\x16' % b'\xAA\xAA\xAA\xAA\xAA')
    #bytearray
    ba = bytearray([0xff, 0x0a])
    print(type(ba), len(ba), ba[0], ba[1])
    tx = bytearray(b'\x90\x00\x00\x00\x00')
    print(tx, tx[0], tx[3])
    #int移位取高低byte, int转bytes
    ReadAddr = 0x010203
    print((ReadAddr >> 16) & 0xFF, ((ReadAddr >> 16) & 0xFF).to_bytes(2, byteorder='big', signed=False))
    byte = bytes.fromhex("{:02x}".format((ReadAddr >> 8) & 0xFF))
    print(byte)
    print((ReadAddr) & 0xFF)

