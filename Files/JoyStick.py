from digitalio import DigitalInOut, Direction, Pull
from adafruit_rgb_display import st7789
import board

class Joystick:
    def __init__(self):
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000000

        self.spi = board.SPI()
        self.disp = st7789.ST7789(
                    self.spi,
                    height=240,
                    y_offset=80,
                    rotation=180,
                    cs=self.cs_pin,
                    dc=self.dc_pin,
                    rst=self.reset_pin,
                    baudrate=self.BAUDRATE,
                    )

        # 버튼 초기화
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT
        self.button_A.pull = Pull.UP

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT
        self.button_B.pull = Pull.UP

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT
        self.button_L.pull = Pull.UP

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT
        self.button_R.pull = Pull.UP

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT
        self.button_U.pull = Pull.UP

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT
        self.button_D.pull = Pull.UP

        self.button_C = DigitalInOut(board.D4)
        self.button_C.direction = Direction.INPUT
        self.button_C.pull = Pull.UP

        # 백라이트 설정
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        self.width = self.disp.width
        self.height = self.disp.height

    def is_pressed(self, button):
        """특정 버튼이 눌렸는지 확인"""
        return not button.value  # 버튼이 눌리면 False -> True로 변환

