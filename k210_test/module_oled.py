from ssd1306k import SSD1306
from machine import I2C
import time

class ClassOLED():

    def __init__(self) -> None:
        i2c = I2C(I2C.I2C0, mode=I2C.MODE_MASTER, scl=27, sda=28)
        print('i2c scan:', i2c.scan())
        self._oled = SSD1306(i2c, addr=0x3c)
        self._oled.fill(0x00)  # 清屏,0x00(白屏)，0xff(黑屏)

    def clear(self):
        self._oled.fill(0x00)

    def show_default(self):
        # 显示字符。参数格式为（str,x,y）,其中x范围是0-127，y范围是0-7（共8行）
        self._oled.text("Hello World!", 0, 0)  # 写入第 0 行内容
        self._oled.text("MicroPython", 0, 2)  # 写入第 2 行内容
        self._oled.text("---------------------", 0, 3)
        self._oled.text("By Rolooc", 50, 4)

    def show_text(self, txt, x, y):
        if len(txt.strip()) == 0:
            raise ValueError('txt empty')
        if x < 0 or x > 127 or y < 0 or y > 7:
            raise ValueError('x(%d) or y(%d) invalid' % (x, y))
        self._oled.text(txt, x, y)

    # @classmethod
    # def test(self):
    #     self._a = 1
    #     print(hasattr(self, '_a'))
    #     print(hasattr(self, '_oled'))
    #     self._oled = 2

    # @classmethod
    # def test2(self):
    #     print(hasattr(self, '_a'))
    #     print(hasattr(self, '_oled'))

if __name__ == '__main__':
    oled_obj = ClassOLED()
    oled_obj.show_default()
    #time.sleep(1)
    #oled_obj.clear()
    #time.sleep(1)
    #oled_obj.show_text('test', 0, 0)
    # ClassOLED.test()
    # ClassOLED.test2()
