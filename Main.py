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
import influx_connect as influx
import csv
from txt2LineProt import txt2Line

# Define MQTT client


broker_address="192.168.0.104"
subscription="domoticz/in"
port=1883
byteCoding="utf-8"


# Check for influx logins

try:
    with open('influx_login.csv', newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        temp=[]
        for row in file:
            temp.append(row)
            
    org=temp[0][0]
    bucket=temp[1][0]
    token=temp[2][0]
    url=temp[3][0]
            
except FileNotFoundError:
    
    print('creating file for logins pleas enter \n')
    org=input('Organisation: ')
    bucket=input('Bucket: ')
    token=input('Token: ')
    url=input('URL: ')
    temp=[[org],[bucket],[token],[url]]
    with open('influx_login.csv','w',newline='') as csvfile:
        file = csv.writer(csvfile, delimiter=' ', quotechar='|')
        for d in temp:
            file.writerow(d)

    

    
org1 = "joseph.battesti@gmail.com"
bucket1 = "joseph.battesti's Bucket"
token1="pTPv99afLaup7TOeaOd5VpaG3P6pmJ22maPxRxqum1x0h0d7VVGMVxyt9DPX9OQ0hKhD2fPg9yFUomfZS8P10g=="
url1="https://us-east-1-1.aws.cloud2.influxdata.com"


conect_sucess=True

try:
   client=MQ.MQTTClient(broker_address,subscription,port,byteCoding)
except :
    print('No device connected')
    conect_sucess=False
    
if conect_sucess:
    esp=ctrl.Controlleur(client)
else:
    esp=0
    

if conect_sucess:
    def print_options():
        print("q : Quit")
        print("v : Print values")
        print("b : Begin data recording")
        print("e : Send saved data to database")
        print("c : Calibrate")
        print("l : Load SD")
        print("s : extract features")
        print("p : Normal transmission protocol to influx")
        
    print_options()
        
    while True:
        try:
            if keyboard.is_pressed('v'):
                while True:
                    print(esp.get_values())
                    try:
                        if keyboard.is_pressed('q'):
                            print_options()
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
                
                data = np.genfromtxt('data.txt',delimiter=',', skip_header=1)
                influx.send_data(data,bucket,org,token,url)
                print("data sent")


        except:
                break
            
else:
    
    def print_options():
        print("q : Quit")
        print("p : SD to influx")
        
    print_options()
    
    while True:
        try:
            if keyboard.is_pressed('q'):
                break
            
            if keyboard.is_pressed('p'):
                path=input('Path du fichier :')
                lines=txt2Line(path)
                influx.send_data(lines,bucket,org,token,url)
                print("data sent")
                break

        except:
                break
    



