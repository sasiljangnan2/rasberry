import spidev
import RPi.GPIO as GPIO
import time

class MCP3202:
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 1000000  # 1MHz
        self.spi.mode = 0

    def read_channel(self, channel):
        if channel not in [0, 1]:
            raise ValueError('Channel must be 0 or 1')

        # MCP3202 command format:
        # First byte: Start bit (1) + SGL/DIFF (1) + D2 + D1 + D0 + X + X + X
        # Second byte: X + X + X + X + X + X + X + X
        # Third byte: X + X + X + X + X + X + X + X
        
        # Start bit = 1
        # SGL/DIFF = 1 (single-ended)
        # D2 = 0
        # D1 = channel
        # D0 = 0
        cmd = [0x06 | (channel << 1), 0, 0]
        
        resp = self.spi.xfer2(cmd)
        
        # Extract the 12-bit value
        # First byte contains 1 unused bit and 7 data bits
        # Second byte contains 5 data bits and 3 unused bits
        value = ((resp[1] & 0x0F) << 8) | resp[2]
        
        return value

    def close(self):
        self.spi.close()

    def get_voltage(self, channel, vref=3.3):
        """
        Read voltage from specified channel
        :param channel: ADC channel (0 or 1)
        :param vref: Reference voltage (default 3.3V)
        :return: Voltage value
        """
        raw_value = self.read_channel(channel)
        voltage = (raw_value * vref) / 4095  # 4095 = 2^12 - 1
        return voltage