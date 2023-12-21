# pyright: reportMissingImports=false

import board
import colours

SSID = "Makerstation"
PWD = "mizmakers"

TIMEOUT = 10.0

BANNER = '''
 _____ _             _ _ _         _   _____ _       
|__   |_|___ ___ ___| | | |___ ___| |_|  |  | |_ ___ 
|   __| | . | -_|  _| | | | . |  _|  _|  |  |   |  _|
|_____|_|_  |___|_| |_____|___|_| |_| |_____|_|_|_|  
        |___|              
V 2.0 alpha
'''

TRACE = False

NTP_OFFSET = 1  # UTC offset
MODE = 'demo'  # 'testing','clock' ,'demo'
DISPLAY_MODE = 'random'  # 'normal','random', 'fancy','all_the_colours', 'rainbow'

LIGHT_SENSOR = True
IR_REMOTE = True

I2C_SCL = board.SCL
I2C_SDA = board.SDA

LED_PIN_CI = board.A1
LED_PIN_DI = board.A0
IR_PIN = board.A2  # Pin connected to IR receiver.

PALLETE = colours.PALLETE_AURORA

LED_MIN_BRIGHTNESS = 0.3
LED_DEFAULT_BRIGHTNESS = .6
LED_NUMBER = 126
