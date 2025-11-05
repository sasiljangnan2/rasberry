import time

import board # RPi.GPIO 대체

import busio # SPI 통신용

import digitalio # CS 핀 제

import adafruit_mcp3xxx.mcp3008 as MCP

from adafruit_mcp3xxx.analog_in import AnalogIn



# SPI 버스 및 CS 핀 설정

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

cs = digitalio.DigitalInOut(board.D8) 



# MCP3008 객체 생성

mcp = MCP.MCP3008(spi, cs)



# channel 0 객체 생성 ('read_adc(0)'을 대체)

chan0 = AnalogIn(mcp, MCP.P0)



while(True):

    # 10비트로 변환하여 출력

    print(chan0.value >> 6) 

    time.sleep(1)