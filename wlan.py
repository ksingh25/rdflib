import machine
import network
import time
from network import WLAN

wlan = network.WLAN(network.STA_IF)

def wlan_connect(ssid='MYSSID', password='MYPASS'):
    if not wlan.active() or not wlan.isconnected():
        wlan.active(True)
        print('connecting to:', ssid)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
            print('.', end='')
            pass
    print('network config:', wlan.ifconfig())

wlan_connect('put-your-WiFi-network-id', 'password')

