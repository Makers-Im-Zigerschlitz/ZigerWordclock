# pyright: reportShadowedImports=false
# pyright: reportMissingImports=false

import supervisor
import time
import settings
import colours


class Ringclock():

    def __init__(self, strip, light_sensor=None):
        self.constants()
        self.strip = strip
        self.light_sensor = light_sensor
        if settings.TRACE:
            print("[function]: Ringclock.__init__()")

    def constants(self):
        self.IT = [0, 1]
        self.IS = [3, 4, 5, 6]
        self.FIVE_TO = [8, 9, 10, 29, 30, 31]
        self.FIVE_PAST = [8, 9, 10, 42, 43]
        self.TEN_TO = [11, 12, 13, 14, 15, 29, 30, 31]
        self.TEN_PAST = [11, 12, 13, 14, 15, 42, 43]
        self.QUARTER_TO = [16, 17, 18, 19, 20, 21, 29, 30, 31]
        self.QUARTER_PAST = [16, 17, 18, 19, 20, 21,  42, 43]
        self.TWENTY_TO = [22, 23, 24, 25, 26, 27, 29, 30, 31]
        self.TWENTY_PAST = [22, 23, 24, 25, 26, 27,  42, 43]
        self.TWENTY_FIVE_PAST = [8, 9, 10, 29, 30, 31, 36, 37, 38, 39, 40]
        self.TWENTY_FIVE_TO = [8, 9, 10, 42, 43, 36, 37, 38, 39, 40]
        self.HALF_PAST = [36, 37, 38, 39, 40]
        self.ONE = [44, 45, 46]
        self.TWO = [47, 48, 49, 50]
        self.THREE = [52, 53, 54]
        self.FOUR = [61, 62, 63, 64, 65]
        self.FIVE = [56, 57, 58, 59]
        self.SIX = [66, 67, 68, 69, 70, 71]
        self.SEVEN = [72, 73, 74, 75, 76]
        self.EIGHT = [83, 84, 85, 86, 87]
        self.NINE = [77, 78, 79, 80, 81]
        self.TEN = [88, 89, 90, 91, 92, 93]
        self.ELEVEN = [95, 96, 97, 98]
        self.TWELVE = [103, 104, 105, 106, 107, 108]
        self.HOURS = [self.TWELVE,  self.ONE,  self.TWO,  self.THREE,  self.FOUR,  self.FIVE,
                      self.SIX,  self.SEVEN,  self.EIGHT,  self.NINE,  self.TEN,  self.ELEVEN]
        self.MINUTES = [[], self.FIVE_PAST, self.TEN_PAST,  self.QUARTER_PAST,  self.TWENTY_PAST,  self.TWENTY_FIVE_PAST,
                        self.HALF_PAST,  self.TWENTY_FIVE_TO,  self.TWENTY_TO,  self.QUARTER_TO,  self.TEN_TO,  self.FIVE_TO]
        self.FIVE_MINUTES = [[], [124], [124, 125],
                             [124, 125, 121], [124, 125, 121, 123]]
        self.CLOCK = [103, 104, 105]
        self.WIFI = 122
        self.MIZ = [114, 115, 116]
        self.CON_ERROR = [5, 30, 49, 53, 62]
        self.NTP_ERROR = [25, 28, 49, 53, 62]
        self.GEN_ERROR = [49, 53, 62]

    def clear(self):
        if settings.TRACE:
            print("[function]: Ringclock.clear()")
        for i in range(settings.LED_NUMBER):
            self.strip[i] = (0, 0, 0)

    def notify(self, col):
        if settings.TRACE:
            print("[function]: Ringclock.notify()")
        self.strip[self.WIFI] = col
        self.strip.show()

    def error(self, e):
        if "No network" in str(e):
            col = colours.RED
            word = self.CON_ERROR
        else:
            col = colours.ORANGE
            word = self.GEN_ERROR
        if settings.TRACE:
            print("[function]: Ringclock.error()")
        self.clear()
        self.strip[self.WIFI] = col
        for i in word:
            self.strip[i] = col
        self.strip.show()
        print(e)
        time.sleep(1)
        if "No network" in str(e):
            supervisor.reload()

    def start_animation(self):
        if settings.TRACE:
            print("[function]: Ringclock.start_animation()")
        self.strip[self.MIZ[0]] = settings.PALLETE[0]
        self.strip[self.MIZ[1]] = settings.PALLETE[1]
        self.strip[self.MIZ[2]] = settings.PALLETE[2]
        self.strip.show()

    def show(self, h, m, s, mode='normal'):
        if settings.TRACE:
            print(f"[function]: Ringclock.show({h},{m},{s},{mode})")
        self.clear()
        # Stunden
        if m >= 25:
            h += 1
        h = h % 12
        if mode == 'normal':
            self.set_normal(h, m)
        if mode == 'random':
            self.set_random(h, m)
        if mode == 'fancy':
            self.set_fancy(h, m)
        if mode == 'all_the_colours':
            self.set_all_the_colours(h, m)
        if mode == 'rainbow':
            self.set_rainbow(h, m)

        if settings.LIGHT_SENSOR == True:
            brightness = self.light_sensor.lux / 100
            if brightness <= settings.LED_MIN_BRIGHTNESS:
                brightness = settings.LED_MIN_BRIGHTNESS
            self.strip.brightness = brightness
            if settings.TRACE:
                print(f"[brightness]: {self.strip.brightness}")
        self.strip.show()

    def binary(self, h, m, s):
        if settings.TRACE:
            print(f"[function]: Ringclock.binary({h},{m},{s})")
        self.clear()
        pass

    def set_normal(self, h, m):
        if settings.TRACE:
            print(f"[function]: set_normal({h},{m})")
        for i in self.HOURS[h]:
            self.strip[i] = settings.PALLETE[2]
        # Minuten (Worte)
        mins = int((m) / 5)
        for i in self.MINUTES[mins]:
            self.strip[i] = settings.PALLETE[1]

        # Minuten (Punkte)
        mins = m % 5
        for i in self.FIVE_MINUTES[mins]:
            self. strip[i] = settings.PALLETE[1]

        for i in self.IT:
            self.strip[i] = settings.PALLETE[0]
        for i in self.IS:
            self.strip[i] = settings.PALLETE[0]

    def set_random(self, h, m):
        if settings.TRACE:
            print(f"[function]: set_random({h},{m})")
        for i in self.HOURS[h]:
            self.strip[i] = colours.rnd(i)
        mins = int((m) / 5)
        for i in self.MINUTES[mins]:
            self.strip[i] = colours.rnd(i)
        mins = m % 5
        for i in self.FIVE_MINUTES[mins]:
            self.strip[i] = colours.rnd(i)
        for i in self.IT:
            self.strip[i] = colours.rnd(i)
        for i in self.IS:
            self.strip[i] = colours.rnd(i)

    def set_fancy(self, h, m):
        if settings.TRACE:
            print(f"[function]: set_fancy({h},{m})")
        for i in self.HOURS[h]:
            self.strip[i] = colours.fancy(i)
        mins = int((m) / 5)
        for i in self.MINUTES[mins]:
            self.strip[i] = colours.fancy(i)
        mins = m % 5
        for i in self.FIVE_MINUTES[mins]:
            self.strip[i] = colours.fancy(i)
        for i in self.IT:
            self.strip[i] = colours.fancy(i)
        for i in self.IS:
            self.strip[i] = colours.fancy(i)

    def set_all_the_colours(self, h, m):
        if settings.TRACE:
            print(f"[function]: set_all_the_colours({h},{m})")
        for i in self.HOURS[h]:
            self.strip[i] = colours.all_the_colours(i)
        mins = int((m) / 5)
        for i in self.MINUTES[mins]:
            self.strip[i] = colours.all_the_colours(i)
        mins = m % 5
        for i in self.FIVE_MINUTES[mins]:
            self.strip[i] = colours.all_the_colours(i)
        for i in self.IT:
            self.strip[i] = colours.all_the_colours(i)
        for i in self.IS:
            self. strip[i] = colours.all_the_colours(i)

    def set_rainbow(self, h, m):
        if settings.TRACE:
            print(f"[function]: set_rainbow({h},{m})")
        for i in self.HOURS[h]:
            self.strip[i] = colours.rainbow(i)
        mins = int((m) / 5)
        for i in self.MINUTES[mins]:
            self.strip[i] = colours.rainbow(i)
        mins = m % 5
        for i in self.FIVE_MINUTES[mins]:
            self.strip[i] = colours.rainbow(i)
        for i in self.IT:
            self.strip[i] = colours.rainbow(i)
        for i in self.IS:
            self.strip[i] = colours.rainbow(i)
