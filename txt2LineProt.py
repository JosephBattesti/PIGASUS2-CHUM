# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 13:30:33 2022

@author: JoJo
"""
import csv
import datetime

def txt2Line(path):
    with open(path, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open('temp.csv', 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)
            
    with open('temp.csv','r',newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=' ', quotechar='|')
        lines=[]
        for row in file:
            
            vals=[s.strip() for s in row[1].split(',')]
            #heure minute secodes
            hms=[int(s.strip()) for s in vals[0].split(':')]
            #annee mois jour
            amj=[int(s.strip()) for s in row[0].split('-')]
            #milisecondes
            ms=0
            
            #----Correction pour avoir 2022 04 15. A eliminer !-----
            amj[0]=2022
            amj[1]=4
            amj[2]=15
            #-------------------------------------------------------
            
            t=datetime.datetime(amj[0],amj[1],amj[2],hms[0],hms[2],hms[2],ms)
            unix_timestamp = int(datetime.datetime.timestamp(t)*1000000000)
            
            tag=vals[2]
            param=vals[3]
            value=vals[4]
            
            l="values"+ ",type="+tag+ " "+param+"=" + value + " " + str(unix_timestamp)
            
            lines.append(l)
            
    thefile = open('Values2Influx.txt', 'w')
    for item in lines:
        thefile.write("%s\n" % item)
        
    return lines