import board

SSID = "SSID"
PWD = "password"

TIMEOUT = 10.0

BANNER = '''
 _____ _             _ _ _         _   _____ _       
|__   |_|___ ___ ___| | | |___ ___| |_|  |  | |_ ___ 
|   __| | . | -_|  _| | | | . |  _|  _|  |  |   |  _|
|_____|_|_  |___|_| |_____|___|_| |_| |_____|_|_|_|  
        |___|              
V 1.0
'''

TIMEZONE="Europe/Zurich"

LIGHT_SENSOR = True
I2C_SCL = board.SCL
I2C_SDA = board.SDA

LED_PIN_CI = board.A1
LED_PIN_DI = board.A0
IR_PIN = board.A2  # Pin connected to IR receiver.

LED_COLOUR_OFF = (0, 0, 0)
LED_COLOUR_RED = (255, 0, 0)
LED_COLOUR_YELLOW = (255, 150, 0)
LED_COLOUR_ORANGE = (255, 40, 0)
LED_COLOUR_GREEN = (0, 255, 0)
LED_COLOUR_TEAL = (0, 255, 120)
LED_COLOUR_CYAN = (0, 255, 255)
LED_COLOUR_BLUE = (0, 0, 255)
LED_COLOUR_PURPLE = (180, 0, 255)
LED_COLOUR_MAGENTA = (255, 0, 20)
LED_COLOUR_WHITE = (255, 255, 255)

LED_COLOUR_MINUTE = LED_COLOUR_GREEN
LED_COLOUR_HOUR = 0xFF1200
LED_COLOUR_TEXT = (0, 125, 124)

LED_MIN_BRIGHTNESS = 0.3
LED_DEFAULT_BRIGHTNESS = .6
LED_NUMBER = 126

 