from datetime import datetime
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision
import numpy as np
import time
import datetime
presentDate = datetime.datetime.now()
unix_timestamp = int(datetime.datetime.timestamp(presentDate)*1000000000)
t0=unix_timestamp # ns

step=100000000 #100ms en ns
time1 = time.time()

data = np.genfromtxt('acceleration_mouvement.csv',delimiter=',', skip_header=1)

acc_x = data[:, 0]
acc_y = data[:, 1]
acc_z = data[:, 2]
mag_x = data[:, 3]
mag_y = data[:, 4]
mag_z = data[:, 5]
gyro_x = data[:, 6]
gyro_y = data[:, 7]
gyro_z = data[:, 8]

# You can generate an API token from the "API Tokens Tab" in the UI
token = "ekU2uRUeLYJUNuJm9oHxFWD4NMNmKBkcTd5DLiOf6YiG-OS_l06i503apoGfuNCPo_oWmIHVJx32jbIaWJiuLQ=="
org = "emilegag05@gmail.com"
bucket = "Python_test"

with InfluxDBClient(url="https://us-central1-1.gcp.cloud2.influxdata.com", token=token, org=org) as client:
   write_api = client.write_api(write_options=SYNCHRONOUS)

tag = "acc_x,device=LSM9DS1 ACC_X="

send_data = np.array([])
i = 0
while i < len(acc_x):
   timestamp = t0 + step*i
   send_data = np.append(send_data, tag + str(acc_x[i]) + " " + str(timestamp))
   i+=1

print(send_data)
write_api.write(bucket, org, send_data)
print(time.time()-time1)

client.close()
