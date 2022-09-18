import words
import wifi
import socketpool
import adafruit_requests
import time
import rtc
import ssl
import adafruit_dotstar
import settings
import busio
import supervisor


# time.localtime indices
HOUR = 3
MINUTE = 4
SECOND = 5

if settings.LIGHT_SENSOR == True:
    import adafruit_bh1750
    i2c = busio.I2C(settings.I2C_SDA,settings.I2C_SCL)
    light_sensor = adafruit_bh1750.BH1750(i2c)

strip = adafruit_dotstar.DotStar(settings.LED_PIN_CI, settings.LED_PIN_DI, settings.LED_NUMBER, brightness=settings.LED_DEFAULT_BRIGHTNESS, auto_write=False)
realtc = rtc.RTC()


def set_time():
    print(f"Stopping station")
    radio = wifi.radio
    radio.stop_station()

    strip[words.WIFI] = settings.LED_COLOUR_BLUE
    strip.show()

    radio.start_station()
    print(f"Trying to connect to {settings.SSID} using {settings.PWD}")
    
    try:
        radio.connect(settings.SSID, settings.PWD,timeout=10.0)
        strip[words.WIFI] = settings.LED_COLOUR_GREEN
        strip.show()
    except ConnectionError as e:
        strip[words.WIFI] = settings.LED_COLOUR_RED
        strip.show()
        print(e)
        supervisor.reload()


    print("connected")
    time.sleep(1)

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    time_URL = f"http://worldtimeapi.org/api/timezone/{settings.TIMEZONE}"

    print(f"Getting time from {time_URL}")
    try:
        response = requests.get(time_URL)
    except Exception as e:
        strip[words.WIFI] = settings.LED_COLOUR_ORANGE
        strip.show()
        print(e)
        supervisor.reload()

    if response.status_code == 200:
        realtc.datetime = time.localtime(response.json()['unixtime']
                                    + response.json()['dst_offset']
                                    + response.json()['raw_offset'])
        print(f"System Time: {realtc.datetime}")
    else:
        print("Setting time failed")
        strip[words.WIFI] = settings.LED_COLOUR_ORANGE
        time.sleep(1)
        strip.show()
        supervisor.reload()

    print("Switching off WiFi")
    radio.stop_station()

def get_simple_time():
    hour = realtc.datetime[HOUR]
    minute = realtc.datetime[MINUTE]
    second = realtc.datetime[SECOND]
    print(f"{hour}:{minute}:{second}")
    return hour, minute, second


def clear_clockface():
    for i in range(settings.LED_NUMBER):
        strip[i] = (0, 0, 0)


def test_strip():
    for i in range(settings.LED_NUMBER):
        if i%10 == 0:
            strip[i] = settings.LED_COLOUR_HOUR
        elif i%5 == 0:
            strip[i] = settings.LED_COLOUR_MINUTE
        else:
            strip[i] = settings.LED_COLOUR_TEXT
    time.sleep(1)
    strip.show()

def set_clockface(h, m,):
    clear_clockface()
    # Stunden
    if m >= 25:
        h += 1
    h = h % 12
    for i in words.HOURS[h]:
        strip[i] = settings.LED_COLOUR_HOUR

    # Minuten (Worte)
    mins = int((m) / 5)
    for i in words.MINUTES[mins]:
        strip[i] = settings.LED_COLOUR_MINUTE

    # Minuten (Punkte)
    mins = m % 5
    for i in words.FIVE_MINUTES[mins]:
        strip[i] = settings.LED_COLOUR_MINUTE

    for i in words.IT:
        strip[i] = settings.LED_COLOUR_TEXT
    for i in words.IS:
        strip[i] = settings.LED_COLOUR_TEXT

    if settings.LIGHT_SENSOR == True:
        brightness = light_sensor.lux / 100
        if brightness <= settings.LED_MIN_BRIGHTNESS:
            brightness = settings.LED_MIN_BRIGHTNESS
        strip.brightness = brightness
    print(strip.brightness)
    strip.show()


def main():
    print(settings.BANNER)
    
    print(f"Clearing clockface")
    clear_clockface()
    set_time()

    print("selftest...")
    test_strip()
    time.sleep(0.75)

    print(time.localtime())

    while True:
        print(realtc.datetime)
        hour, minute, second = get_simple_time()
        set_clockface(hour, minute)
        time.sleep(10)

        if hour == 23 and minute == 59 and second <= 10:
            set_time()

if __name__ == "__main__":
    main()
