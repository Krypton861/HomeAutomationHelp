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

# Specify the path to your JSON file
configFilePath = 'sensorConfig.json'
outputFilePath = 'snw.json'        #"Sensor NetWork" 


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



#######
####### START LOGIK um aus "Format": x;x;1;x;16;x - Zu echtem String: "30 ; 4 ; 1 ; 0 ; 16 ; 1 ; 1704212964.92", zu matchen
####### Und dann z.b. daraus Status und Thermometer zu extrahieren
#######

#Logik um aus "Format": x;x;1;x;16;x - Zu echtem String: "30 ; 4 ; 1 ; 0 ; 16 ; 1 ; 1704212964.92", zu matchen
def compareString(Format, stringToCheck):
    # Sieht wie magic aus. Ist einfach nur ein (';') um ein array zu generieren. Und danach strip um formatierung zu garantieren (ohne WHite spaces)
    # Convert to int ist nicht möglich wegen dem x
    formatArray = [element.strip() for element in Format.split(';')]
    stringArray = [element.strip() for element in stringToCheck.split(';')]

    #Check ob beide Arrays gleich lang sing -> gleich viele ';' Also vergleichbar
    if len(formatArray) != len(stringArray):
        print(f"Error with length of String to check VS Format String in Config: Format (len:{len(formatArray)}) {formatArray} | stringToCheck (len: {len(stringArray)}): {stringArray}")
        return False
    
    successFlag = False
    #Iterere einzeln über jeden WErt im FormatArray -> x;x;1;x;16;x und vergleiche
    for index, formatRule in enumerate(formatArray):
        #Ignoeriere alles was ein X hat -> Nur die "richtigen" Werte werden angeschaut
        if(formatRule != 'x'):
            #Bei einem Wert - Vergleiche Format mit String
            if(formatArray[index] == stringArray[index]):
                successFlag = True
            else:
                #Sofortiger Abbruch, da es nicht matchen kann.
                return False 
        #print(index, formatArray[index], stringArray[index])

    #Brauchen Flag, damit bei ausschließlich X es nicht "Erfolg" melldet. Bei missmatch wird sofort mit False abgebrochen
    if(successFlag):
        return True
    
    return False


def checkSensorTyp(stringToCheck):
    #Im Json Objekt hole alles was unter "Sensortyp" steht.
    typeData = configData["Sensortyp"]

    #Iteriere über alle Elemente. z.b. Element 0 = 'Status' Element 1 = 'x;x;1;x;16;x'
    for elem in typeData.items():
        result = compareString(elem[1],stringToCheck)
        if(result):
            #print(f"{stringToCheck} - Ist Type: {elem[0]}")
            return elem[0]

    return "Unknown" 

def checkObjektTyp(stringToCheck):
    #Im Json Objekt hole alles was unter "Sensortyp" steht.
    typeData = configData["Objekt"]

    #Sonder Condition für Baterie. Da die ChildID mit Batterie überschrieben wird. 
    #Daher check for 255 auf 2. String und wenn setze "einfach" auf 0 weil Sensor Typ hier nicht bestimmt wird.
    if([element.strip() for element in stringToCheck.split(';')][1] == "255"):
        #Da es die 255 im richtigen bzw. zweiten Element gibt -> replace first 255 mit 0
        stringToCheck = stringToCheck.replace('255', '0', 1) 

    #Iteriere über alle Elemente. z.b. Element 0 = 'Status' Element 1 = 'x;x;1;x;16;x'
    for elem in typeData.items():
        result = compareString(elem[1],stringToCheck)
        if(result):
            #print(f"{stringToCheck} - Ist Type: {elem[0]}")
            return elem[0]

    return "Unknown" 

#######
####### ENDE LOGIK um aus "Format": x;x;1;x;16;x - Zu echtem String: "30 ; 4 ; 1 ; 0 ; 16 ; 1 ; 1704212964.92", zu matchen
####### Und dann z.b. daraus Status und Thermometer zu extrahieren
#######



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


    #######
    ####### Config Laden und input String auswerten
    #######

    # Open the file and load the JSON data
    with open(configFilePath, 'r') as file:
        configData = json.load(file)
    
    ### DEBUG - PRINT : Convert the dictionary to a JSON string to print or use another Way
    #json_string = json.dumps(configData, indent=2)
    #print(json_string)

    #Haupt Funktionen, die oben Def. sind verwenden wir hier um die Auswertung des Sensor und Objekt zu erhalten.
    sensorType = checkSensorTyp(ts_daten)
    objectType = checkObjektTyp(ts_daten)
    #print(f"{ts_daten} \t- Ist SensorType: {sensorType} \t ObjectType: {objectType}")


    #Wenn NodeName nicht bekannt ist, wird "Unknown" returned -> Error weil es in dem Lookup table nicht existiert.
    #Wird aktueller loop einfach hier beendet und wieder weiter im while true
    if(sensorType == "Unknown" or objectType == "Unknown"):
        print(f"Error: Input String konnte nicht zugeordnet werden \t {ts_daten} \t- SensorType: {sensorType} \t ObjectType: {objectType}")
        continue
    

    # Unser neues Daten Objekt erzeugen, was wir jetzt schreiben wollen.
    newData = {
        objectType:{
            sensorType:{
                "Wert": ts_daten[5],
                "zeitstempel": jetzt_postgres,
            }
        }
    }



    #######
    #######  Alles vorbereitet. Jetzt Output json Datei öffnen und ersetzen oder einfach hinzufügen. Jeh nachdem was es schon gobt.
    #######

    #Wenn die Datei nicht existiert oder Leer ist -> Fehler abfangen
    try:
        # Open the file and load the JSON data into the variable jsonData
        with open(outputFilePath, 'r') as file:
            jsonData = json.load(file)
    except:
        jsonData = {}

    #Wenn es unser Objekt schon gibt -> Finden des Elements um zu Modifizieren
    if objectType in jsonData:
        #Wenn es in unserem Objekt auch den Sensor Typen schon gibt -> Ersetze das INNERE des Objektes
        if sensorType in jsonData[objectType]:
            jsonData[objectType][sensorType] = newData[objectType][sensorType]             
            #print(f"Sensor Typ {sensorType} exists für ObjectType {objectType} in jsonData {json.dumps(jsonData[objectType][sensorType], indent=2)}")
        
        #Wenn es in unserem Objekt den Sensor Typen NICHT gibt -> Ersetze das INNERE des Objektes
        else:
            jsonData[objectType].update(newData[objectType]) #Mit Update fügt man ein Element ins Dictinary ein 
            #print(f"Sensor Typ {sensorType} DOES NOT EXIST für ObjectType {objectType} in jsonData {json.dumps(jsonData[objectType], indent=2)}")

    #Wenn es unser Objekt noch NICHT gibt -> Hinzufügen mit samt Sensor Type
    else:
        jsonData.update(newData) #Mit Update fügt man ein Element ins Dictinary ein 
        #print(f"Added Element to curr Dict: {json.dumps(jsonData, indent=2)}")


    ### DEBUG - PRINT : Convert the dictionary to a JSON string to print or use another Way
    #json_string = json.dumps(jsonData, indent=2)
    #print(json_string)
        

    # Zum Schluss das veränderte Json Objekt wieder in die gleiche Datei laden. Dabei wird einfach alles überschrieben, egal was.
    with open(outputFilePath, "w") as json_file:
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




	
