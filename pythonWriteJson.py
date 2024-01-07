import json

for x in range(1):

    #######
    ####### NEUES JSON FORMAT START - Daten Check und verwandlung in Volltext Namen
    #######

    inputData = "20 ; 255 ; 3 ; 0 ; 0 ; 100 ; 1573315199.67"
    filePath = 'output.json'
    jetzt_postgres = "2022-01-05 12:34:56"

    # Unsere Übersetzungstabelle welche Kombination aus NodeID und ChildID zu welchem Volltext Namen führen.
    lookupTable =  {
        20: {
            0: "MobilesThermometerTemperatur",
            255: "MobilesThermometer_2",
        },
        21:{
            0:"Carport",
            255:"Carport_2"
        },
        22:{
            0:"Kellertreppe",
            255:"Kellertreppe_2"
        },
        30:{
            0:"Zisterne_1",
            1:"Zisterne_2",
            2:"Zisterne_3",
            3:"Zisterne_4",
            4:"Zisterne_5",
            255:"Zisterne_6"
        },
        40:{
            0:"Speisekammer",
            255:"Speisekammer_2"
        },
        41:{
            0:"Gästeklo",
            255:"Gästeklo_2"
        },
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

    #Beginnend mit einem String wo alle Daten drinnen sind.
    ts_daten = inputData.split(';')

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
