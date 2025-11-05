from mcp3202 import MCP3202
import time

def main():
    # MCP3202 인스턴스 생성
    adc = MCP3202()

    try:
        while True:
            # 채널 0의 전압 읽기
            voltage0 = adc.get_voltage(0)
            # 채널 1의 전압 읽기
            voltage1 = adc.get_voltage(1)

            print(f"Channel 0: {voltage0:.3f}V")
            print(f"Channel 1: {voltage1:.3f}V")
            print("-" * 20)

            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        adc.close()

if __name__ == '__main__':
    main()