from Maix import I2S
from Maix import GPIO
from fpioa_manager import *
import audio, time

'''播放wav'''
# # register i2s(i2s0) pin
# fm.register(34,fm.fpioa.I2S0_OUT_D1)
# fm.register(35,fm.fpioa.I2S0_SCLK)
# fm.register(33,fm.fpioa.I2S0_WS)

# # init i2s(i2s0)
# wav_dev = I2S(I2S.DEVICE_0)
# # config i2s according to audio info
# wav_dev.channel_config(
#     wav_dev.CHANNEL_1, I2S.TRANSMITTER,
#     resolution = I2S.RESOLUTION_16_BIT,
#     cycles = I2S.SCLK_CYCLES_32,
#     align_mode = I2S.RIGHT_JUSTIFYING_MODE,
# )

# # init audio
# player = audio.Audio(path = "/sd/voice/jinyiding.wav")
# player.volume(100)

# # read audio info
# wav_info = player.play_process(wav_dev)
# print("wav info", wav_info)
# sample_rate = wav_info[1]
# print("wav sample rate", sample_rate)
# wav_dev.set_sample_rate(sample_rate)

# # loop to play audio
# while True:
#     ret = player.play()
#     print('play ret', ret)
#     if ret == None:
#         print("format error")
#         break
#     elif ret==0:
#         print("end")
#         break
# player.finish()

'''录音+播放'''
# 音频使能IO
AUDIO_PA_EN_PIN = 32
fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)
audio_en = GPIO(GPIO.GPIO1, GPIO.OUT, value=1)

fm.register(20,fm.fpioa.I2S0_IN_D0)
fm.register(19,fm.fpioa.I2S0_WS)
fm.register(18,fm.fpioa.I2S0_SCLK)

fm.register(34,fm.fpioa.I2S2_OUT_D1)
fm.register(35,fm.fpioa.I2S2_SCLK)
fm.register(33,fm.fpioa.I2S2_WS)

sample_rate = 44*1000

rx = I2S(I2S.DEVICE_0)
rx.channel_config(rx.CHANNEL_0, rx.RECEIVER, align_mode = I2S.STANDARD_MODE)
rx.set_sample_rate(sample_rate)

tx = I2S(I2S.DEVICE_2)
tx.channel_config(tx.CHANNEL_1, tx.TRANSMITTER, align_mode = I2S.RIGHT_JUSTIFYING_MODE)
tx.set_sample_rate(sample_rate)

while True:
    # audio = rx.record(256)#sampling points number must be smaller than 256
    # print(audio, type(audio), audio.to_bytes())
    # tx.play(audio)
    record = rx.record(256)
    record_data = record.to_bytes()
    print(record, record_data)
    record_audio = audio.Audio(record_data)
    print(record_audio)
    # wav_info = record_audio.play_process(tx)
    # tx.play(play_audio)