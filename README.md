# ZigerWordclock V2

CircuitPython Sourcecode für unsere Wordclock.

## Dateien

### settings_ziger.py

Einstellungen für die Ziger-Wort-Uhr.
Muss umbenannt werden in `settings.py`

Hier lassen sich Zeitzone, Farben, Microcontrollerpins und ähnliches einstellen.

### code.py

Hauptprogramm.

Beim Einschalten verbindet sich die Wordclock kurz über WLAN über ntp die Zeit zu holen.
Danach wird Wifi ausgeschaltet und und die Zeit im RTC des Microcontroller gespeichert.
Alle 10 Sekunden wird die Zeit aus dem RTC gelesen und die LEDs entsprechend ein- oder ausgeschaltet.
Immer um die im `settings.py` bei `SYNCH_TIME` angegebene Zeit wird wieder versucht über WiFi die Zeit zu synchronisieren und ausserdem geprüft ob Sommer- oder Winterzeit ist.

## ziger_wordclock.py

Enthält die Implementation der eigentlichen Ziger-Wort-Uhr.

## ringclock.py

Enthält eine Implementation einer Uhr mit einem 60 LED langen Neopixelring. (WIP)

## Tools

Zwei CircuitPython-Programme, eins um alle sichtbaren WLANs aufzulisten, eins um IR-Codes einzulesen und zu testen. 

## lib

Benötigte Bibliotheken.