# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:45:48 2022

@author: JoJo
"""

import keyboard
import time
import mqttClass as MQ
import controlleur as ctrl
import numpy as np


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
print("b : Begin data recording")
print("e : Send saved data to database")
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

        if keyboard.is_pressed('d'):
            while True:
                np.savetxt('saved_data.csv',esp.get_values() , delimiter=',')
                try:
                    if keyboard.is_pressed('q'):
                        break
                except:
                        break

        if keyboard.is_pressed('e'):
            token = "ekU2uRUeLYJUNuJm9oHxFWD4NMNmKBkcTd5DLiOf6YiG-OS_l06i503apoGfuNCPo_oWmIHVJx32jbIaWJiuLQ=="
            org = "emilegag05@gmail.com"
            bucket = "Python_test"


    except:
            break
    




