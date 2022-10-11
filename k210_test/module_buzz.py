import time
from machine import Timer,PWM

CONST_BUZZ_PIN = 15

#循环发出不同频率响声。
BUZZ_FREQ_BASIC_ARRAY = [0,523,578,659,698,784,880,988,1080,]
BUZZ_MUSIC_ARRAY = [
[3,1],[3,0.5],[2,0.5],[3,2],
[3,0.5],[5,0.5],[3,0.5],[2,0.5],[3,2],
[1,1],[1,0.5],[2,0.5],[3,0.5],[5,0.5],[3,1],
[2,1],[2,0.5],[1,0.5],[2,2],
]

BUZZ_FREQ_OK_ARRAY = [3000, 2000]
BUZZ_FREQ_ERR_ARRAY = [3000]

class ClassBuzz():

    def __init__(self, timer, pin):
        self._timer = timer
        self._beep = PWM(timer, freq=BUZZ_FREQ_BASIC_ARRAY[1], duty=50, pin=pin)
        self._beep.disable()

    def play_jht(self):
        for i in range(len(BUZZ_MUSIC_ARRAY)):
            self._beep.enable()
            self._beep.freq(BUZZ_FREQ_BASIC_ARRAY[BUZZ_MUSIC_ARRAY[i][0]])
            time.sleep(BUZZ_MUSIC_ARRAY[i][1])
            self._beep.disable()
            time.sleep(0.02)

    def play_ok(self):
        for i in range(len(BUZZ_FREQ_OK_ARRAY)):
            self._beep.enable()
            self._beep.freq(BUZZ_FREQ_OK_ARRAY[i])
            time.sleep(0.5)
            self._beep.disable()

    def play_err(self):
        for i in range(len(BUZZ_FREQ_ERR_ARRAY)):
            self._beep.enable()
            self._beep.freq(BUZZ_FREQ_ERR_ARRAY[i])
            time.sleep(1)
            self._beep.disable()

if __name__ == '__main__':
    timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
    buzz = ClassBuzz(timer, CONST_BUZZ_PIN)
    buzz.play_err()
    time.sleep(1)
    buzz.play_ok()
    time.sleep(1)
    buzz.play_jht()
