import board
import busio
import digitalio
from adafruit_mcp3xxx.mcp3202 import MCP3202
from adafruit_mcp3xxx.analog_in import AnalogIn

# SPI 버스 생성
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# CS 핀 설정
cs = digitalio.DigitalInOut(board.D5)  # CE0를 사용할 경우 board.CE0

# MCP3202 생성
mcp = MCP3202(spi, cs)

# 아날로그 입력 채널 설정
chan0 = AnalogIn(mcp, MCP3202.P0)
chan1 = AnalogIn(mcp, MCP3202.P1)

try:
    while True:
        # 전압과 raw 값 읽기
        print(f'채널 0: 전압 = {chan0.voltage:.2f}V, Raw 값 = {chan0.value}')
        print(f'채널 1: 전압 = {chan1.voltage:.2f}V, Raw 값 = {chan1.value}')
        print('-' * 30)
        
except KeyboardInterrupt:
    print('\n프로그램 종료')