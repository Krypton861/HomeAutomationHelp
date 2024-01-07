import json

#inputData = "20 ; 255 ; 3 ; 0 ; 0 ; 100 "
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
    #print(typeData)

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
    #print(typeData)

    #Iteriere über alle Elemente. z.b. Element 0 = 'Status' Element 1 = 'x;x;1;x;16;x'
    for elem in typeData.items():
        result = compareString(elem[1],stringToCheck)
        if(result):
            #print(f"{stringToCheck} - Ist Type: {elem[0]}")
            return elem[0]

    return "Unknown" 


###
### Eigentlicher Start des Programms
###

# Specify the path to your JSON file
configFilePath = 'sensorConfig.json'

# Open the file and load the JSON data
with open(configFilePath, 'r') as file:
    configData = json.load(file)
  
### DEBUG - PRINT : Convert the dictionary to a JSON string to print or use another Way
#json_string = json.dumps(configData, indent=2)
#print(json_string)

for element in inputData:
    sensorType = checkSensorTyp(element)
    objectType = checkObjektTyp(element)
    print(f"{element} \t- Ist SensorType: {sensorType} \t ObjectType: {objectType}")



