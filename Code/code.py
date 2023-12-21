# pyright: reportShadowedImports=false
# pyright: reportMissingImports=false

import wifi
import socketpool
import time
import rtc
import adafruit_dotstar
import settings
import colours
import adafruit_ntp
import random

from ziger_wordclock import Wordclock

strip = adafruit_dotstar.DotStar(settings.LED_PIN_CI, settings.LED_PIN_DI,
                                 settings.LED_NUMBER, brightness=settings.LED_DEFAULT_BRIGHTNESS, auto_write=False)
realtc = rtc.RTC()
dts = -1

if settings.LIGHT_SENSOR == True:
    import adafruit_bh1750
    import busio
    i2c = busio.I2C(settings.I2C_SDA, settings.I2C_SCL)
    light_sensor = adafruit_bh1750.BH1750(i2c)
else:
    light_sensor = None

clockface = Wordclock(strip, light_sensor)


def set_manual_time(y, m, d, h, mi=0, s=0):
    if settings.TRACE:
        print("[function]: set_manual_time()")
    print(f"[set_manual_time]: Stopping station")
    radio = wifi.radio
    radio.stop_station()
    t = time.struct_time((y, m, d, h, mi, s, -1, -1, -1))
    ut = time.mktime(t)
    realtc.datetime = time.localtime(ut)


def set_time():
    global dts
    if settings.TRACE:
        print("[function]: set_time()")
    print(f"[set_time]: Stopping station")
    radio = wifi.radio
    radio.stop_station()

    clockface.notify(colours.BLUE)

    radio.start_station()
    print(f"[set_time]:Trying to connect to {
          settings.SSID} using {settings.PWD}")

    try:
        radio.connect(settings.SSID, settings.PWD, timeout=settings.TIMEOUT)
        clockface.notify(colours.GREEN)
        strip.show()
    except ConnectionError as e:
        clockface.error(e)

    print("[set_time]: connected")
    time.sleep(1)

    pool = socketpool.SocketPool(wifi.radio)

    print(f"[set_time]: Getting time from NTP. ntp offset: {
          settings.NTP_OFFSET}, dts: {dts}")
    ntp = adafruit_ntp.NTP(pool, tz_offset=settings.NTP_OFFSET+dts)
    try:
        realtc.datetime = ntp.datetime
    except Exception as e:
        clockface.error(e)

    print("[set_time]: Switching off WiFi")
    radio.stop_station()


def get_dts_cet():
    global dts
    if settings.TRACE:
        print("[function]: get_dts()")
    print("[get_dts]: Checking for daylight saving time")
    yearday = realtc.datetime.tm_yday
    year = realtc.datetime.tm_year

    # Trust me, bro, this should work for Switzerland
    # see excel table in the repo
    if is_leap_year(year):
        if yearday - (yearday-1) % 7 >= 85 and yearday - (yearday+2) % 7 <= 299:
            dts = 1
        else:
            dts = 0
    else:
        if yearday - (yearday) % 7 >= 84 and yearday - (yearday+3) % 7 <= 298:
            dts = 1
        else:
            dts = 0
    print(f"[get_dts]: dts: {dts}")
    print(f"[get_dts]: yearday: {yearday - (yearday+3) % 7}")


def is_leap_year(year):
    if settings.TRACE:
        print("[function]: is_leap_year()")
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True


def get_simple_time():
    global dts
    if settings.TRACE:
        print("[function]: get_simple_time()")
    hour = realtc.datetime.tm_hour + dts
    minute = realtc.datetime.tm_min
    second = realtc.datetime.tm_sec
    print(f"[get_simple_time]: {hour}:{minute}:{second}")
    return hour, minute, second


def test_strip():
    if settings.TRACE:
        print("[function]: test_strip()")
    for i in range(settings.LED_NUMBER):
        if i % 10 == 0:
            strip[i] = settings.PALLETE[0]
        elif i % 5 == 0:
            strip[i] = settings.PALLETE[1]
        else:
            strip[i] = colours.rainbow(i)
    time.sleep(1)
    strip.show()


def run_clock():
    print(settings.BANNER)
    print(f'[clock]: Running in mode: {settings.MODE}')
    print(f'[clock]: Displaymode: {settings.DISPLAY_MODE}')
    print(f"[clock]: Clearing clockface")
    clockface.clear()
    clockface.start_animation()

    get_dts_cet()
    set_time()

    while True:
        try:
            hour, minute, second = get_simple_time()

            if hour == 3 and minute == 00 and second <= 10:
                get_dts_cet()
                set_time()

            clockface.show(hour, minute, second, settings.DISPLAY_MODE)
            time.sleep(10)

            if settings.MODE == 'demo':
                if second <= 10:
                    ch = random.randint(0, 3)
                    if ch == 0:
                        colours.PALLETE_RANDOM = colours.rand_pallete()
                        settings.PALLETE = colours.PALLETE_RANDOM
                        print('[Demomode]: New random pallete')
                    if ch == 1:
                        settings.PALLETE = random.choice(colours.PALS)
                        print('[Demomode]: Changed pallete')
                    if ch == 2:
                        settings.DISPLAY_MODE = random.choice(
                            ['normal', 'random', 'fancy', 'all_the_colours'])
                        print(f'[Demomode]: New displaymode: {
                              settings.DISPLAY_MODE}')
                    if ch == 3:
                        colours.rand_setup()
                        print('[Demomode]: Changed random colours')
        except Exception as e:
            clockface.error(e)


if __name__ == "__main__":
    if settings.MODE == 'demo':
        test_strip()
        time.sleep(1)
        run_clock()
    if settings.MODE == 'clock':
        run_clock()
    if settings.MODE == 'testing':
        settings.PALLETE = colours.PALLETE_AURORA
        print("selftest...")
        test_strip()
        time.sleep(0.75)
