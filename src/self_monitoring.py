#!/usr/bin/env python3
VERSION = "0.10"

import os
import glob
import time
import signal
import sys
import configparser
import paho.mqtt.client as mqtt_client


### -= Classes =-
class mqtt(mqtt_client.Client):
    def __init__(self, client_id=""):
        super().__init__(client_id)
        self.device_id = client_id

    def publish(self, topic, payload=None, precision=0):
        if (isinstance(payload, float)):
            # payload="{:.2f}".format(payload)
            payload = "{1:,.{0}f}".format(precision, payload)
        super().publish("tele/"+self.device_id+"/"+topic, payload, qos=1, retain=True, properties=None)


### -= Functions =-


### -= Program initialization =-
def init():
    signal.signal(signal.SIGINT, signal.default_int_handler)
    print("VERSION", VERSION)
    print(time.strftime("%H:%M:%S %d/%m/%Y", time.localtime()))
    try:
        # os.environ.get("MQTT_SERVER")
        MQTT_SERVER = os.environ["MQTT_SERVER"]
        MQTT_PORT = os.environ["MQTT_PORT"]
        MQTT_USER = os.environ["MQTT_USER"]
        MQTT_PASS = os.environ["MQTT_PASS"]
    except KeyError as ke:
        print("No environment variable {0}. Exit...".format(ke), end="\n\n")
        sys.exit()
    # print(MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASS)

    config_file = os.path.basename(__file__)[:os.path.basename(__file__).rindex(".")]+".ini"
    global config
    config = configparser.ConfigParser()
    config.read(config_file)

    global DELAY
    DELAY = int(config["MAIN"]["Delay"])
    global client
    DEVICE_ID = config["MAIN"]["DeviceID"]
    client = mqtt(DEVICE_ID)
    client.username_pw_set(MQTT_USER, MQTT_PASS)
    client.connect(host=MQTT_SERVER, port=MQTT_PORT)
    # client.publish("tele/"+device_id+"/Connected", time.strftime("%H:%M:%S %d/%m/%Y", time.localtime()))
    client.publish("Connected", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
    client.loop_start()


### -= Program starts =-
def main():
    sec_start = time.time()
    while True:
        try:
            tFile = open('/sys/class/thermal/thermal_zone0/temp')
            tempC = float(tFile.read())/1000.0
            print('%3.1f°C' % tempC)
            client.publish("CPU_Temp", tempC, 1)
            client.publish("LastUpdate", time.strftime("%d/%m/%Y %H:%M:%S", time.localtime()))
            time.sleep(DELAY)
        except KeyboardInterrupt:
            print(" : Ctrl+C pressed, bye.", end="\n\n")
            sys.exit()
    sec_end = time.time()
    sec = sec_end-sec_start
    print(sec)


###
init()
main()
