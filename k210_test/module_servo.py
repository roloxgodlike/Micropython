import time
from machine import Timer, PWM
from fpioa_manager import fm
from Maix import GPIO


class CONST_SERVO:
    _90_PIN = 17
    _360_PIN = 33
    PWM_FREQ_HZ = 50
    PWM_PERIOD_MS = (1000 / PWM_FREQ_HZ)
    _360_DIRECT_CLOCKWISE = 0
    _360_DIRECT_ANTI_CLOCKWISE = 1
    _360_CLOCKWISE_S5 = 1
    _360_CLOCKWISE_S4 = 1.1
    _360_CLOCKWISE_S3 = 1.2
    _360_CLOCKWISE_S2 = 1.3
    _360_CLOCKWISE_S1 = 1.4
    _360_STOP = 1.5
    _360_ANTI_CLOCKWIS_S1 = 1.6
    _360_ANTI_CLOCKWIS_S2 = 1.7
    _360_ANTI_CLOCKWIS_S3 = 1.8
    _360_ANTI_CLOCKWIS_S4 = 1.9
    _360_ANTI_CLOCKWIS_S5 = 2.0


class ClassServo():

    def __init__(self, timer, pin):
        self._timer = timer
        self._servo = PWM(
            self._timer, freq=CONST_SERVO.PWM_FREQ_HZ, duty=0, pin=pin)
        self._servo.disable()

    # 按频率计算高电平所占ms对应的百分比
    def _ms_to_duty(self, ms):
        return ms / CONST_SERVO.PWM_PERIOD_MS * 100

     # 0.5ms-0°|1ms-45°|1.5ms-90°|2ms-135°|2.5ms-180° 按角度计算占空比(%)
    def _angle_to_duty(self, angle):
        ms = 0.5 + ((angle / 180) * 2)
        print('angle_to_duty-ms:', ms)
        return self._ms_to_duty(ms)

    def exec_90_angle(self, angle):
        self._servo.enable()
        duty = self._angle_to_duty(angle)
        print('exec_90_angle angle:', angle, 'duty:', duty)
        self._servo.duty(duty)

    def exec_360_ms(self, ms):
        self._servo.enable()
        if ms < CONST_SERVO._360_CLOCKWISE_S5:
            ms = CONST_SERVO._360_STOP
        elif ms > CONST_SERVO._360_ANTI_CLOCKWIS_S5:
            ms = CONST_SERVO._360_STOP
        print('exec_360_ms ms:', ms)
        self._servo.duty(self._ms_to_duty(ms))

    def exec_360_mode(self, mode):
        self._servo.enable()
        # if speed < 1:
        #     speed = 0
        # elif speed > 5:
        #     speed = 5
        # if speed == 0:
        #     ms = CONST_SERVO._360_STOP
        # else:
        #     if direct == CONST_SERVO._360_DIRECT_ANTI_CLOCKWISE:
        #         ms = 1 + speed / 10
        #     else:
        #         ms = 1.5 + speed / 10
        print('exec_360_direct_speed mode:', mode)
        self._servo.duty(self._ms_to_duty(mode))


if __name__ == '__main__':
    servo_90 = ClassServo(
        Timer(Timer.TIMER0, Timer.CHANNEL1, mode=Timer.MODE_PWM), CONST_SERVO._90_PIN)
    servo_360 = ClassServo(
        Timer(Timer.TIMER1, Timer.CHANNEL0, mode=Timer.MODE_PWM), CONST_SERVO._360_PIN)
    mode = CONST_SERVO._360_CLOCKWISE_S5
    # while True:
    #     servo_360.exec_360_mode(mode)
    #     mode += 0.1
    #     if mode > CONST_SERVO._360_ANTI_CLOCKWIS_S5: mode = CONST_SERVO._360_CLOCKWISE_S5

    #     servo_90.exec_90_angle(0)
    #     time.sleep(1)
    #     servo_90.exec_90_angle(45)
    #     time.sleep(1)
    #     servo_90.exec_90_angle(90)
    #     time.sleep(1)
    #     servo_90.exec_90_angle(135)
    #     time.sleep(1)
    #     servo_90.exec_90_angle(180)
    #     time.sleep(1)

    angle = 0
    direct = 0

    def key_test_cb(KEY):
        global angle, direct, mode
        time.sleep_ms(10)
        if KEY_TEST.value() == 0:
            if angle >= 180 or angle <= 0:
                direct = not direct
            if direct:
                angle += 45
            else:
                angle -= 45
            servo_90.exec_90_angle(angle)
            servo_360.exec_360_mode(mode)
            mode += 0.1
            if mode > CONST_SERVO._360_ANTI_CLOCKWIS_S5:
                mode = CONST_SERVO._360_CLOCKWISE_S5

    fm.register(16, fm.fpioa.GPIOHS0)
    KEY_TEST = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)
    KEY_TEST.irq(key_test_cb, GPIO.IRQ_FALLING)
