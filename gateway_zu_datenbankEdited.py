# -*- encoding: utf-8 -*-


import serial
import os
import datetime
import csv
import psycopg2
import json


# Definitionen
# Logfiles sollten nach RAMDISK. Das ewige Logfile sollte regelmässig per Cron-Job gesichert werden.
csv_datei = "/mnt/RAMDISK/snw.csv"
port = serial.Serial('/dev/ttyUSB0')


#Initialisation
port.baudrate = 57600
port.bytesize = 8
port.flushInput()


# Initialisation der Datenbank
#CONNECTION = "postgres://localhost:5432/sensornetzwerk"
CONNECTION = "dbname=sensornetzwerk user=pi password=pi host=localhost port=5432"
conn = psycopg2.connect(CONNECTION)
cur = conn.cursor()

# zu Beginn neue CSV-Datei anlegen
with open(csv_datei, 'w') as f:
   f.write('')


# Ewige Schleife
while True:                                                      

    # Port lesen
    ser_bytes = port.readline()
    
    # aktuelle Zeit seit 1.1.1970 bestimmen und fuer CSV in String umwandeln, fuer Postgres reicht der Zeitstempel
    jetzt_csv = str((datetime.datetime.now() - datetime.datetime(1970,1,1)).total_seconds()) 
    jetzt_postgres = datetime.datetime.now()
    
    # serielle Daten lesen
    daten = ser_bytes      

    # so etwas wie \n filtern                                     
    daten = daten.strip()                                       

    # Für Debugzwecke
    #print (daten)

    # am Semikolon zerhacken, in Liste schreiben
    # das hier kann Python 3 nicht mehr, k.A. warum
    daten = daten.split(";")                                    

    # Für Debugzwecke
    # print (daten)

    # den oben erzeugten String des Datums hinten an die Liste schreiben
    # insert waere vorne: daten.insert(0,jetzt_csv);                                      
    daten.append(jetzt_csv)


    # ts_daten ist ein Array, das aus der UART-Mitteilung und dem Zeitstempel besteht
    # MySensors-Mitteilungsformat siehe https://www.mysensors.org/download/serial_api_20
    # ts_daten[0] ... NodeID
    # ts_daten[1] ... ChildID
    # ts_daten[2] ... Command
    # ts_daten[3] ... Ack
    # ts_daten[4] ... Type
    # ts_daten[5] ... Payload
    # ts_daten[6] ... Zeitstempel
    # Beispiele
    # 20 ;   0 ; 1 ; 0 ; 0 ; 22.7 ; 1573315199.13
    # 20 ; 255 ; 3 ; 0 ; 0 ; 100 ; 1573315199.67
    ts_daten = daten                                            

   
    #######
    ####### NEUES JSON FORMAT START - Daten Check und verwandlung in Volltext Namen
    #######

    filePath = 'output.json'

    # Unsere Übersetzungstabelle welche Kombination aus NodeID und ChildID zu welchem Volltext Namen führen.
    lookupTable =  {
        20: {
            0: "MobilesThermometer",
            255: "MobilesThermometer_2",
        },
        21:{
            0:"Carport",
            255:"Carport_2"
        } ,
        22:{
            0:"Kellertreppe",
            255:"Kellertreppe_2"
        } ,
        30:{
            0:"Zisterne_1",
            1:"Zisterne_2",
            2:"Zisterne_3",
            3:"Zisterne_4",
            4:"Zisterne_5",
            255:"Zisterne_6"
        } ,
        40:{
            0:"Speisekammer",
            255:"Speisekammer_2"
        } ,
        41:{
            0:"Gästeklo",
            255:"Gästeklo_2"
        } ,
        42:{
            0:"Terasse",
            255:"Terasse_2"
        } ,
        43:{
            0:"Bad1",
            255:"Bad1_2"
        } ,
        44:{
            0:"Bad2",
            255:"Bad2_2"
        } ,
        45:{
            0:"SchlafzimmerM",
            255:"SchlafzimmerM_2"
        } ,
    }

    #######
    ####### Erstmal input Daten auswerten und verwerten. Sowie alle Checks durchführen
    #######

    #Hole den Wert der NodeID ChildID um aus dem LookupTable den korrekten Namen zu erhalten
    NodeName = lookupTable.get(int(ts_daten[0])).get(int(ts_daten[1]))

    #Wenn NodeName nicht bekannt ist, wird Null oder None hinzugefügt. -> Error weil es in dem Lookup table nicht existiert.
    #Wird aktueller loop einfach hier beendet und wieder weiter im while true
    if(NodeName is None):
        print("NodeID,ChildID Benennung ist nicht hinterlegt. ABBRUCH!")
        #raise Exception("NodeID,ChildID Benennung ist nicht hinterlegt. ABBRUCH!")
        continue

    #Der Wert des elements ts_daten[0] und ts_daten[1] für Debug zwecke - wird printet
    #nodeID= int(ts_daten[0]); childID = int(ts_daten[1]); print("nodeID:",nodeID," | childID:",childID

    # Unser neues Daten Objekt erzeugen, was wir jetzt schreiben wollen.
    newData = {
        "name": NodeName,
        "payload": ts_daten[5]+" REPLACED",
        "zeitstempel": jetzt_postgres,
    }

    #######
    #######  Alles vorbereitet. Also jetzt json Datei öffnen und hinzufügen oder ersetzen.
    #######

    # Open the file and load the JSON data into the variable jsonData
    with open(filePath, 'r') as file:
        jsonData = json.load(file)

    nodeIsMissingInFile = True
    #eine foreach schleife. Schaue jedes Element in der jsonData einzeln an. Jede iteration heißt das aktuelle element item.
    #Und wir suchen ja nach einer übereinstimmung im namen also check item['name']. Anschließend ersetze es mit den vorbereiteten Daten
    for index, item in enumerate(jsonData):
        if item['name'] == NodeName:
            jsonData[index] = newData   # Replace the entire element with new data. !! VORSICHT. MUSS GLEICHES FORMAT HABEN WIE DATEI !!
            nodeIsMissingInFile = False   #Flag damit wir nicht an die Datei hinzufügen müssen
            break   #Wird nur ein element zum ersetzen geben.

    #Sollte die Flag unverändert sein gibt es die Node noch nicht -> Hinzufügen
    if(nodeIsMissingInFile):
        jsonData.append(newData)

    ### DEBUG - PRINT : Convert the dictionary to a JSON string to print or use another Way
    #json_string = json.dumps(jsonData, indent=2)
    #print(json_string)

    # Zum Schluss das veränderte Json Objekt wieder in die gleiche Datei laden. Dabei wird einfach alles überschrieben, egal was.
    with open(filePath, "w") as json_file:
        json.dump(jsonData, json_file, indent=2)

    #######
    ####### NEUES JSON FORMAT ENDE
    #######

    # Werte in Datenbank schreiben
    SQL = "INSERT INTO sensorwerte (zeitstempel, node_id, child_id, command, ack, type, payload) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    try:
        data = (jetzt_postgres, ts_daten[0], ts_daten[1],ts_daten[2],ts_daten[3],ts_daten[4],ts_daten[5],)  
        cur.execute(SQL, data)
    except (Exception, psycopg2.Error) as error:
        print(error.pgerror)
    conn.commit()




	
