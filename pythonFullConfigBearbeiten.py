import json

inputData = [
    "21 ; 255 ; 0 ; 0 ; 17 ; 02.03.2001",
    "21 ; 255 ; 3 ; 0 ; 6 ; 0",
    "21 ; 255 ; 3 ; 0 ; 11 ;Temperature Sensor",
    "21 ; 255 ; 3 ; 0 ; 12 ; 1.0 ",
    "42 ; 0   ; 1 ; 0 ; 16 ; 0  ",
    "42 ; 255 ; 3 ; 0 ; 0 ; 0 ",
    "22 ; 255 ; 3 ; 0 ; 21 ; 0 ",
    "21 ; 255 ; 3 ; 0 ; 21 ; 0 ",
    "44 ; 0   ; 1 ; 0 ; 16 ; 0 ",
    "44 ; 255 ; 3 ; 0 ; 0 ; 94 ",
    "40 ; 0   ; 1 ; 0 ; 16 ; 0 ",
    "40 ; 255 ; 3 ; 0 ; 0 ; 64 ",
    "45 ; 0   ; 1 ; 0 ; 16 ; 0 ",
    "45 ; 255 ; 3 ; 0 ; 0 ; 100 ",
    "43 ; 0   ; 1 ; 0 ; 16 ; 0 ",
    "43 ; 255 ; 3 ; 0 ; 0 ; 12 ",
    "30 ; 255 ; 3 ; 0 ; 21 ; 0 ",
    "21 ; 0   ; 1 ; 0 ; 0 ; 07.F ",
    "21 ; 255 ; 3 ; 0 ; 0 ; 100 ",
    "22 ; 0   ; 1 ; 0 ; 0 ; 07.M ",
    "22 ; 255 ; 3 ; 0 ; 0 ; 89 ",
    "41 ; 0   ; 1 ; 0 ; 16 ; 0 ",
    "41 ; 255 ; 3 ; 0 ; 0 ; 28 ",
    "30 ; 1   ; 1 ; 0 ; 16 ; 0 ",
    "30 ; 2   ; 1 ; 0 ; 16 ; 0 ",
    "30 ; 3   ; 1 ; 0 ; 16 ; 0 ",
    "30 ; 4   ; 1 ; 0 ; 16 ; 1 ",
    "30 ; 0   ; 1 ; 0 ; 35 ; 99 "
]



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



for ts_daten in inputData:

    #######
    ####### NEUES JSON FORMAT START - Daten Check und verwandlung in Volltext Namen
    #######

    # Specify the path to your JSON file
    configFilePath = 'sensorConfig.json'
    outputFilePath = 'snw.json'        #"Sensor NetWork" 
    jetzt_postgres = "2022-01-05 12:34:56"

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
        
    ####### NEUES JSON FORMAT ENDE
    #######
