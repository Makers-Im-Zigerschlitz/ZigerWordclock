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

### colours.py

Alles was mit den Farben zusammenhängt.

### settings.py

Die Einstellungen 

## Einstellung im Detail

### Netzwerk 

* SSID:     SSID des WLANs
* PWD:      Password des WLANs
* TIMEOUT:  Timeout für die WLAN Verbindung

### UHR

* NTP_OFFSET: Zeitdifferenz zu GMT, bei uns 1
* MODE:
    * wordclock: Normaler Modus, die Zigerwordclock zeigt die Zeit im eingestellten DISPLAY_MODE.
    * testing: schaltet alle LEDs ein, zum testen.
    * demo: Schaltet kurz alle LEDs ein, und wechselt danach alle Minuten entweder DISPLAY_MODE oder Farben.
* DISPLAY_MODE:
    * normal: ÄS ISCH wird in der ersten, die Minuten in der zweiten und die Stunde in der dritten Farbe der ausgewählten Pallete angezeigt
    * random: Jede LED kriegt eine zufällige Farbe aus `colours.COLS`, die entsprechenden Zeichen leuchten dann in dieser Farbe. Diese Farben können mit `colours.rand_colours` neu gewürfelt werden. 
    * fancy: Jede LED kriegt der Reihe nach eine der Farben aus der gewählten Pallete.
    * all_the_colours: Jede LED kriegt der Reihe nach eine der Farben aus `colours.COLS`.
    * rainbow: Jede LED kiegt seine Farbe mit der `rainbowio.colorwheel()`

* LIGHT_SENSOR: `True` wenn der Lichtsensor gebraucht werden soll, `False` wenn nicht.
* IR_REMOTE: `True` wenn der IR-Empfänger gebraucht werden soll, `False` wenn nicht. (Noch nicht implementiert)

* PALLETE: Die gewünschte Farbpalette aus `colours.py` 

* LED_MIN_BRIGHTNESS: minimale Helligkeit (wenn der Lichtsensor gebraucht wird)
* LED_DEFAULT_BRIGHTNESS maximale Helligkeit


## Tools

Zwei CircuitPython-Programme, eins um alle sichtbaren WLANs aufzulisten, eins um IR-Codes einzulesen und zu testen. 

## lib

Benötigte Bibliotheken.