# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:17:49 2022

@author: JoJo
"""

import keyboard
import csv
import time
import numpy as np
from tempfile import NamedTemporaryFile
import shutil

class Controlleur(object):
    'Class pour un bidule'
    def __init__(self,MQTTclient):
        self.ID=[]
        self.offset=[]
        self.slope=[]
        self.calibrated=False
        #Declare MQTT client for conexion with ESPeasy
        self.client=MQTTclient
        #Check in coefficient.csv if  ID is present with calibration values
        self.loadCalibration()
        
    
    def get_ID(self):
        return self.ID
    
    def loadCalibration(self):
        print('Loading')
        while type(self.ID)!=int:
            self.ID=self.client.get_ID(timeout=.1)
        print('L identifiant du controlleur connecte est: '+str(self.client.get_ID(timeout=.1)))
            
        with open('coefficients.csv', newline='') as csvfile:
            file = csv.reader(csvfile, delimiter=' ', quotechar='|')
            if len(list(file)) == 0:
                print("Le fichier des calibrations est vide")
            else:
                ## Ajoutee "with open" parceque le fichier se ferme apres le if. Verifier print(f.closed)=True
                with open('coefficients.csv', newline='') as csvfile:
                    file = csv.reader(csvfile, delimiter=' ', quotechar='|')
                    for row in file:
                        if len(row)!=0:
                            if float(row[0])==self.ID:
                                coeffs=[float(i) for i in row[1:]]
                                self.offset=coeffs[0:3]
                                self.slope=coeffs[3:6]
                                self.calibrated=True
                                print("Calibration retrouvee")
            
        if not self.calibrated:
            print("Aucune calibration ne correspond a cet ID. SVP ajouter une calibration")
                    
    def get_Calibration(self):
        return self.offset,self.slope
    
    def isCalibrated(self):
        return self.calibrated
    
    def saveCalibration(self):
        if not self.isCalibrated():      
            with open('coefficients.csv', 'a', newline='') as csvfile:
                file = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                file.writerow([self.ID]+self.offset+self.slope)
            print("calibration sauvgardee")
            self.calibrated=True
        else:
            filename = 'coefficients.csv'
            tempfile = NamedTemporaryFile(mode='w', delete=False)
            with open(filename, 'r') as csvfile, tempfile:
                reader = csv.reader(csvfile,delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer = csv.writer(tempfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    if len(row)!=0:
                        if float(row[0]) == self.ID:
                            print('OverWriting calibration for ID:', self.ID)
                            row = [self.ID]+self.offset+self.slope
                        writer.writerow(row)
                        
            shutil.move(tempfile.name, filename)
            self.calibrated=True
            
    def get_values(self,timeout=.1):
        if len(self.client.get_values(timeout))!=0:
            if self.calibrated:
                values=list(np.round((np.array(self.client.get_values(timeout))-np.array(self.offset))*np.array(self.slope),2))
            else: 
                values=self.client.get_values(timeout)
            return values
        else:
            return [0,0,0]
    
    def get_raw_values(self,timeout=.1):
        if len(self.client.get_values(timeout))!=0:
            return self.client.get_values(timeout)
        else:
            return [0,0,0]
        
            
    def calibrate(self,timeout=.1):
        
        #Off set : Mesurer zero point pour x et y lorsque z=1g
        #Off set : Mesurer q1=+1g et q2=-1g pour tous. 
        #slope=abs((q1-q2)/(rawq1-rawq2))
        
        zeropoint=[]
        askedMeasurement = False
        axis=0
        g=1
        
        while True :
            values=self.client.get_values(timeout)
            if len(values)!=0:   
                if not askedMeasurement:
                    if axis==2:
                        print('Apuiller sur s pour mesurer zero en z')  
                    if axis==1:
                        print('Apuiller sur s pour mesurer zero en y')
                    if axis==0:
                        print('Apuiller sur s pour mesurer zero en x')
                    askedMeasurement = True
                try:
                    if keyboard.is_pressed('s'):
                        print('Valeur enregistree :'+str(values[axis]))
                        zeropoint.append(values[axis])
                        askedMeasurement=False
                        axis+=1
                        time.sleep(1)
                    
                    if keyboard.is_pressed('q'):
                        break
                except:
                    break
                if len(zeropoint)==3:
                    print('Zeropoint calibrated sucess:'+str(zeropoint))
                    self.offset=zeropoint
                    break
                
        gMeasure=[]
        askedMeasurement = False
        axis=0
                
        while True :
            values=self.client.get_values(timeout)
            if len(values)!=0:   
                if not askedMeasurement:
                    if axis==2:
                        print('Apuiller sur s pour mesurer 1g en z')  
                    if axis==1:
                        print('Apuiller sur s pour mesurer 1g en y')
                    if axis==0:
                        print('Apuiller sur s pour mesurer 1g en x')
                    askedMeasurement = True
                try:
                    if keyboard.is_pressed('s'):
                        print('Valeur enregistree :'+str(values[axis]))
                        gMeasure.append(values[axis])
                        askedMeasurement=False
                        axis+=1
                        time.sleep(1)
                        
                    if keyboard.is_pressed('q'):
                        break
                except:
                    break
                if len(gMeasure)==3:
                    try:
                        self.slope=list(np.round(abs(g/(np.array(gMeasure)-np.array(zeropoint))),2))
                        print('slope calibrated sucess:'+str(self.slope))
                    except ZeroDivisionError:
                        print("Zero division. Retry calibration with slightly different values")
                    break
                
        if len(gMeasure)==3 and len(zeropoint)==3:
            self.saveCalibration()
        