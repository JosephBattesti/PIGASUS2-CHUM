# PIGASUS2-CHUM
Python tools for acquisition (MQTT from espeasy), processing and transmission to influxDB, of sensor data in pneumatic transport system at CHUM hospital

The code is structured as follows :

* coefficients.csv stores calibration parameters associated to the microcontroller’s ID 
* influx_login.cv stores the organisation, bucket, token, url for the connection to influx
* Main.py is in charge of  :
  - All the displays in the application’s terminal (List of options and sensor values)
  - Input from the user ( Choosing options or entering logins)
  - Checking Connection to MQTT (1883 port default)
  - Checking Logins for InfluxDB in csv file.

* Connectroller.py is the class representing the microcontroller :
  - An object Controller has an ID, calibration parameters and a MQTT Client from which to listen to messages from the physical microcontroller. The class has some important methods : 
  - loadCalibration() :  Checks for the presence of the ID in coefficients.csv in order to upload values. If not found, the user is advised to perform a calibration.
  - calibrate() : Execute the protocol for accelerometer calibration, measuring 1g and 0g  in each  axis (x,y,z) and stores values in coefficients.csv
  - get_values(): Uses calibration parameters in order to correct raw values.
  - get_raw_values(): Listen to the MQTT client.

* mqttClass.py is the class for the MQTT client, implementing the paho library. Check documentation for more information.  The class has attributes such as : 
  - Address,port and subscriptions  for mqtt connections
  - ID and Values for storing and sharing to controller
  - The method onMessage() : Decodes the MQTT message at arrival when a controller object is listening.  The message is byte coded (json for decoding) and has to splitted at every ‘;’ character. This function would have to be developed when more values than acceleration are coming. For now the message is composed of Microcontroller ID and accelerometer values. 
* txt2LineProt.py is used for formatting data coming from the SD card to line protocol format used by InfluxDB. This code is highly dependent on the initial format of the SD data.
* Influx_connect.py sends the line protocol data to the cloud specified by the logins in the csv file.
