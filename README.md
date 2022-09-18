# ZigerWordclock

CircuitPython7 Sourcecode für unsere Wordclock.

## Dateien

### settings.py

Einstellungen.

Hier lassen sich Zeitzone, Farben, Microcontrollerpins und ähnliches einstellen.

### code.py

Hauptprogramm.

Beim einschalten verbindet sich die Wordclock kurz über WLAN zu http://worldtimeapi.org/ und holt sich die Zeit für die eingestellte Zeitzone.
Danach wird Wifi ausgeschaltet und und die Zeit im RTC, des Microcontroller gespeichert. Alle 10 Sekunden wird die Zeit aus dem RTC gelesen und die LEDs entsprechend ein- oder ausgeschaltet.

### words.py

Die LED-Nummern für die verschiedenen Worte.

## Tools

Zwei CircuitPython-Programme, eins um alle sichtbaren WLANs aufzulisten, eins um IR-Codes einzulesen und zu testen. 

## lib

Benötigte Bibliotheken.