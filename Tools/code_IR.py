import pulseio
import adafruit_irremote
import settings
import adafruit_dotstar
import time


print('IR listener')
# Fuzzy pulse comparison function:
def fuzzy_pulse_compare(pulse1, pulse2, fuzzyness=0.2):
    if len(pulse1) != len(pulse2):
        return False
    for i in range(len(pulse1)):
        threshold = int(pulse1[i] * fuzzyness)
        if abs(pulse1[i] - pulse2[i]) > threshold:
            return False
    return True

# Create pulse input and IR decoder.
pulses = pulseio.PulseIn(settings.IR_PIN, maxlen=200, idle_state=True)
decoder = adafruit_irremote.GenericDecode(pulses)
pulses.clear()
pulses.resume()



pixels = adafruit_dotstar.DotStar(settings.LED_PIN_CI, settings.LED_PIN_DI, settings.LED_NUMBER, brightness=settings.LED_DEFAULT_BRIGHTNESS, auto_write=True)


if not settings.IR_LEARN:
    # Loop waiting to receive pulses.
    while True:
        # Wait for a pulse to be detected.
        detected = decoder.read_pulses(pulses,blocking_delay=0.1)
        print('got a pulse...')
        # Got a pulse, now compare.
        if fuzzy_pulse_compare(settings.IR_1, detected):
            print('Recieved ON')
            pixels.brightness = 0.1
        if fuzzy_pulse_compare(settings.IR_2, detected):
            print('Recieved OFF')
            pixels.brightness = 0            
        if fuzzy_pulse_compare(settings.IR_3, detected):
            print('Recieved RED')
            pixels.fill(settings.LED_COLOUR_RED)
        if fuzzy_pulse_compare(settings.IR_4, detected):
            print('Recieved GREEN')
            pixels.fill(settings.LED_COLOUR_GREEN)
        
else:
    while True:
        detected = decoder.read_pulses(pulses)
        print("Heard", len(detected), "Pulses:", detected)
        try:
            code = decoder.decode_bits(detected)
            print("Decoded:", code)
        except adafruit_irremote.IRNECRepeatException:  # unusual short code!
            print("NEC repeat!")
        except adafruit_irremote.IRDecodeException as e:     # failed to decode
            print("Failed to decode: ", e.args)

        print("----------------------------")