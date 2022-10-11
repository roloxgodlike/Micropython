
from Maix import I2S
from Maix import GPIO
from fpioa_manager import *
import audio
import sensor
import lcd
import time


# 音频使能IO
AUDIO_PA_EN_PIN = 32
fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
audio_en = GPIO(GPIO.GPIO1, GPIO.OUT, value=0)

# register i2s(i2s0) pin
fm.register(34, fm.fpioa.I2S0_OUT_D1)
fm.register(35, fm.fpioa.I2S0_SCLK)
fm.register(33, fm.fpioa.I2S0_WS)

# init i2s(i2s0)
wav_dev = I2S(I2S.DEVICE_0)
# config i2s according to audio info
wav_dev.channel_config(
    wav_dev.CHANNEL_1, I2S.TRANSMITTER,
    resolution=I2S.RESOLUTION_16_BIT,
    cycles=I2S.SCLK_CYCLES_32,
    align_mode=I2S.RIGHT_JUSTIFYING_MODE,
)

def _play_wav(name):
    global wav_dev, audio_en

    wav_path = '/sd/voice/{}.wav'.format(name)
    print('wav path', wav_path)

    # init audio
    wav_audio = audio.Audio(path=wav_path)
    wav_audio.volume(100)

    # read audio info
    wav_info = wav_audio.play_process(wav_dev)
    print("wav info", wav_info)
    print("wav sample rate", wav_info[1])
    wav_dev.set_sample_rate(wav_info[1])

    audio_en.value(1)
    # loop to play audio
    while True:
        ret = wav_audio.play()
        if ret == None:
            print("audio err")
            break
        elif ret == 0:
            print("audio done")
            break
    wav_audio.finish()
    audio_en.value(0)

# 摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)  # 后置模式，所见即所得

# lcd初始化
lcd.init()

# 颜色识别阈值 (L Min, L Max, A Min, A Max, B Min, B Max) LAB模型
# 下面的阈值元组是用来识别 红、绿、蓝三种颜色，当然你也可以调整让识别变得更好。
thresholds = [(17, 57, 7, 49, 29, 61),  # 红色阈值 (30, 100, 15, 127, 15, 127)
              (12, 20, -14, -10, 15, 23),  # 绿色阈值(30, 100, -64, -8, -32, 32)
              (0, 30, 0, 64, -128, -20)]  # 蓝色阈值

# _play_wav('jinyiding')

is_processing = 0
last_color = 0
last_ms = 0

def _find_color_after(img, blobs, _color):
    global is_processing, last_color, last_ms

    img.draw_rectangle(blobs[0:4])
    img.draw_cross(blobs[5], blobs[6])
    # img.draw_string(blobs.x(), blobs.y(), _color, color=(255, 255, 0), scale=2)
    img.draw_string(1, 1, _color, color=(255, 255, 0), scale=2)

    if is_processing and last_color != _color:
        return

    if last_color == _color and (time.time() - last_ms < 5):
        return

    is_processing = 1
    last_color = _color
    last_ms = time.time()
    # _play_wav(_color)
    is_processing = 0

def _find_color(img):
    blobs_red = img.find_blobs([thresholds[0]])
    if blobs_red:
        for b in blobs_red:
            _find_color_after(img, b, 'red')

    blobs_green = img.find_blobs([thresholds[1]])
    if blobs_green:
        for b in blobs_green:
           _find_color_after(img, b, 'green')

    # blobs_blue = img.find_blobs([thresholds[2]])
    # if blobs_blue:
    #     for b in blobs_blue:
    #         _find_color_after(img, b, 'blue')

while True:
    img = sensor.snapshot()
    _find_color(img)
    lcd.display(img)  # LCD显示图片
