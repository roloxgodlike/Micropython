from fpioa_manager import fm
from Maix import GPIO
import sensor,lcd,time

GPIO_LED_BLUE = {'pin':12, 'fpioa-group':fm.fpioa.GPIO0, 'gpio_group':GPIO.GPIO0}
GPIO_LED_GREEN = {'pin':13, 'fpioa-group':fm.fpioa.GPIO1, 'gpio_group':GPIO.GPIO1}
GPIO_LED_RED = {'pin':14, 'fpioa-group':fm.fpioa.GPIO2, 'gpio_group':GPIO.GPIO2}
GPIO_KEY_TEST = {'pin':16, 'fpioa-group':fm.fpioa.GPIOHS0, 'gpio_group':GPIO.GPIOHS0}

class ClassGPIO():

    # def _init_gpio_out(self, gpio_pin, gpio_group):
    #     fm.register(gpio_pin, gpio_group)
    #     return GPIO(gpio_group, GPIO.OUT)

    # def _init_gpio_in(self, gpio_pin, gpio_group, in_type):
    #     fm.register(gpio_pin, fm.fpioa.GPIO0)
    #     return GPIO(gpio_group, GPIO.IN, in_type)

    # def _init_gpio_in_irq(self, gpio_obj, cb, irq_typ):
    #     if not isinstance(gpio_obj, GPIO):
    #         raise ValueError('_init_gpio_in_irq need GPIO obj!')
    #     gpio_obj.irq(cb, GPIO.irq_typ)

    def init_led(self):
        fm.register(GPIO_LED_BLUE['pin'], GPIO_LED_BLUE['fpioa-group'])
        self._led_blue = GPIO(GPIO_LED_BLUE['gpio_group'], GPIO.OUT)

        fm.register(GPIO_LED_RED['pin'], GPIO_LED_RED['fpioa-group'])
        self._led_red = GPIO(GPIO_LED_RED['gpio_group'], GPIO.OUT)

        fm.register(GPIO_LED_GREEN['pin'], GPIO_LED_GREEN['fpioa-group'])
        self._led_green = GPIO(GPIO_LED_GREEN['gpio_group'], GPIO.OUT)

    def led_rgb_shutdown(self):
        self._led_blue.value(1)
        self._led_red.value(1)
        self._led_green.value(1)

    def led_rgb_all(self):
        self._led_blue.value(0)
        self._led_red.value(0)
        self._led_green.value(0)

    def led_rgb_blue(self):
        self._led_blue.value(0)
        self._led_red.value(1)
        self._led_green.value(1)

    def led_rgb_red(self):
        self._led_blue.value(1)
        self._led_red.value(0)
        self._led_green.value(1)

    def led_rgb_green(self):
        self._led_blue.value(1)
        self._led_red.value(1)
        self._led_green.value(0)

    def led_at_start(self):
        self.led_rgb_red()

    def led_at_idle(self):
        self.led_rgb_blue()

    def led_at_done(self):
        self.led_rgb_green()

    def init_key(self, cb_func):
        fm.register(GPIO_KEY_TEST['pin'], GPIO_KEY_TEST['fpioa-group'])
        self._key = GPIO(GPIO_KEY_TEST['gpio_group'], GPIO.IN, GPIO.PULL_UP)
        self._key.irq(cb_func, GPIO.IRQ_FALLING)

    def get_key(self):
        return self._key


if __name__ == '__main__':
    gpio_obj = ClassGPIO()
    gpio_obj.init_led()
    gpio_obj.led_at_start()
    time.sleep(1)
    gpio_obj.led_at_idle()
    time.sleep(1)
    gpio_obj.led_at_done()
    gpio_obj.led_rgb_all()
    def key_test_cb(KEY):
        # global g_flag_block
        time.sleep_ms(10)
        if KEY.value() == 0:
            print("key", KEY.value())
        # sensor.shutdown(1)
        # lcd.clear()
        # led_at_start()
        # mBuzz.play_jht()
        # sensor.shutdown(0)
        # g_flag_block = 0
    gpio_obj.init_key(key_test_cb)
    while 1:
        print(gpio_obj._key.value())
        time.sleep(1)

# #GPIO LED
# fm.register(12, fm.fpioa.GPIO0)
# fm.register(13, fm.fpioa.GPIO1)
# fm.register(14, fm.fpioa.GPIO2)
# LED_BLUE = GPIO(GPIO.GPIO0, GPIO.OUT)
# LED_GREEN = GPIO(GPIO.GPIO1, GPIO.OUT)
# LED_RED = GPIO(GPIO.GPIO2, GPIO.OUT)

# #GPIO KEY
# fm.register(16, fm.fpioa.GPIOHS0)
# KEY_TEST = GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)

# def key_test_cb(KEY):
#     global g_flag_block
#     time.sleep_ms(10)
#     print("key-", KEY_TEST.value())
#     sensor.shutdown(1)
#     lcd.clear()
#     led_at_start()
#     mBuzz.play_jht()
#     sensor.shutdown(0)
#     g_flag_block = 0

# KEY_TEST.irq(key_test_cb, GPIO.IRQ_FALLING)
