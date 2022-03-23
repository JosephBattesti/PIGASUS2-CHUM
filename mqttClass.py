# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:48:20 2022

@author: JoJo
"""

import paho.mqtt.client as mqtt
import json

class MQTTClient():
    
    def __init__(self,broker_address,subscription,port,byteCoding):
        self.broker_address=broker_address
        self.subscription=subscription
        self.port=port
        self.byteCoding=byteCoding
        
        self.client = mqtt.Client(subscription)  # Create instance of client with client ID
        self.client.on_connect = self.on_connect  # Define callback function for successful connection
        self.client.on_message = self.on_message  # Define callback function for receipt of a message
        # client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
        self.client.connect(broker_address,port)
        # Buffers for data transmission. Definir autant de variables que d'elements a extraire.
        self.message=[]
        self.ID=[]
        self.values=[]
        
    def on_connect(self,client, userdata, flags, rc):  # The callback for when the client connects to the broker
        print("Connected with sucsess")  # Print result of connection attempt
        self.client.subscribe(self.subscription)  # Subscribe to the topic, receive any messages published on it
        
    def on_message(self,client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
        #Decode message de byte a dictionnaire de strings
        buf=json.loads(msg.payload.decode(self.byteCoding))
        self.message=buf
        #Recupere les valeurs ax ay az dans le 'svalue' et les separer
        vals=[s.strip() for s in buf['svalue'].split(';')]
        vals=[float(s) for s in vals]
        self.values=vals
        #Recuperer ID
        self.ID=buf['idx']
        
    def get_client(self):
        return self.client
    def get_values(self,timeout=.1):
        self.client.loop(timeout)
        return self.values
    def get_ID(self,timeout=.1):
        self.client.loop(timeout)
        return self.ID
    def get_message(self,timeout=.1):
        self.client.loop(timeout)
        return self.message
        
