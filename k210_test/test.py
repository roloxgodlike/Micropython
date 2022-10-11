import sensor
import lcd
import time
import image
import KPU as kpu
from machine import Timer
from module_gpio import *
from module_servo import *
from module_buzz import *
from module_oled import *
import uos

def _unit_test_oled():
    _oled_obj = ClassOLED()
    _oled_obj.show_default()
    time.sleep(2)
    _oled_obj.clear()
    time.sleep(2)
    _oled_obj.show_text('test', 0 , 0)

_gpio_obj = ClassGPIO()
def _unit_test_gpio():
    _gpio_obj.init_led()
    _gpio_obj.led_at_start()
    time.sleep(1)
    _gpio_obj.led_at_idle()
    time.sleep(1)
    _gpio_obj.led_at_done()
    time.sleep(1)

timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
_buzz_obj = ClassBuzz(timer, CONST_BUZZ_PIN)
def _unit_test_buzz():
    _buzz_obj.play_err()
    # _buzz_obj.play_ok()
    # _buzz_obj.play_jht()

def _unit_test_servo():
    _servo_90 = ClassServo(
        Timer(Timer.TIMER0, Timer.CHANNEL1, mode=Timer.MODE_PWM), CONST_SERVO._90_PIN)
    _servo_360 = ClassServo(
        Timer(Timer.TIMER1, Timer.CHANNEL0, mode=Timer.MODE_PWM), CONST_SERVO._360_PIN)
    mode = CONST_SERVO._360_CLOCKWISE_S5

    _servo_360.exec_360_mode(mode)
    mode += 0.1
    if mode > CONST_SERVO._360_ANTI_CLOCKWIS_S5: mode = CONST_SERVO._360_CLOCKWISE_S5

    _servo_90.exec_90_angle(0)
    time.sleep(1)
    _servo_90.exec_90_angle(45)
    time.sleep(1)
    _servo_90.exec_90_angle(90)
    time.sleep(1)
    _servo_90.exec_90_angle(135)
    time.sleep(1)
    _servo_90.exec_90_angle(180)
    time.sleep(1)

def _init_lod_sensor():
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)

    lcd.init()
    task = kpu.load("/sd/model/model.kmodel")
    anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987,
            5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
    kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
    return task

if __name__ == '__main__':
    # _unit_test_servo()
    # _unit_test_oled()
    print(dir(uos))
    print(uos.listdir())

    _unit_test_gpio()
    _unit_test_buzz()

    task = _init_lod_sensor()
    while 1:
        img = sensor.snapshot()
        code = kpu.run_yolo2(task, img)
        if code:
            for i in code:
                print(i)
                img.draw_rectangle(i.rect())
                _gpio_obj.led_at_done()
                _buzz_obj.play_ok()
                img.save("/sd/test.jpg")
                lcd.display(image.Image("/sd/test.jpg"))
                time.sleep(3)
        lcd.display(img)
