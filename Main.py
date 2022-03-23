# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:45:48 2022

@author: JoJo
"""

import keyboard
import time
import mqttClass as MQ
import controlleur as ctrl


# Define MQTT client
broker_address="127.0.0.1"
subscription="domoticz/in"
port=1883
byteCoding="utf-8"
client=MQ.MQTTClient(broker_address,subscription,port,byteCoding)

# Define Controller
esp=ctrl.Controlleur(client)

# Options :

print("q : Quit")
print("v : Print values")
print("c : Calibrate")
print("l : Load SD")
print("s : extract features")
print("p : Normal transmission protocol to influx")

while True:
    try:
        if keyboard.is_pressed('v'):
            while True:
                print(esp.get_values())
                try:
                    if keyboard.is_pressed('q'):
                        break
                except:
                        break
        if keyboard.is_pressed('c'):
                esp.calibrate()     
    except:
            break
    




