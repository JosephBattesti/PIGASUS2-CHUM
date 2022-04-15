# from datetime import datetime
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient

# presentDate = datetime.datetime.now()
# unix_timestamp = int(datetime.datetime.timestamp(presentDate)*1000000000)
# t0=unix_timestamp # ns

# step=1000000000 #1000ms en ns
# time1 = time.time()

def send_data(data,bucket,org,token,url):
    
   with InfluxDBClient(url=url, token=token, org=org) as client:
      write_api = client.write_api(write_options=SYNCHRONOUS)

   write_api.write(bucket, org, data)
   
   print('sent')
   client.close()
   