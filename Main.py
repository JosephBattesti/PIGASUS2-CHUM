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
import connect

# Define MQTT client
broker_address="192.168.0.100"
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

        if keyboard.is_pressed('b'):
            print('savingdata, press q to stop')
            data = np.array([])
            while True:
                read=esp.get_values()
                newdata = str(read[0]) + ', ' + str(read[1]) + ', ' + str(read[2]) + ', '
                with open('data.txt', 'a') as the_file:
                    the_file.write(newdata + '\n')
                print('saved data: ' + str(newdata))
                try:
                    if keyboard.is_pressed('q'):
                        break
                except:
                        break

        if keyboard.is_pressed('e'):
            connect.send_data()
            print("data sent")


    except:
            break
    




