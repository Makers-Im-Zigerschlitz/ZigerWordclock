import wifi, time
from adafruit_binascii import hexlify


def mac_format(b):
    h = hexlify(b).decode()
    return ':'.join(h[i:i+2] for i in range(0,12,2))

while True:
    networks = []
    for network in wifi.radio.start_scanning_networks():
        networks.append(network)
    wifi.radio.stop_scanning_networks()

    networks = sorted(networks, key=lambda net: net.rssi, reverse=True)
    print("-------------")
    for n in networks:
        # MAC,SSID,AuthMode,FirstSeen,Channel,RSSI,CurrentLatitude,CurrentLongitude,AltitudeMeters,AccuracyMeters,Type
        # print(f"{mac_format(n.bssid)},{n.ssid},{n.authmode},,{n.channel},{n.rssi},,,,WIFI")
        print(f"SSID:{n.ssid} RSSI: {n.rssi}")
    # time.sleep(0.)
