# -*- encoding: utf-8 -*-


import serial
import os
import datetime
import csv
import psycopg2

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

    # Für Debugzwecke
    # print
    # print
    # print "Empfangene Datenliste:"
    # print (ts_daten)

    # Neue Daten (Liste von Werten)
    neue_daten = []  
    for i in range (0,7):
      neue_daten.append(str(ts_daten[i]))

    # Suchstring ("echter" String)
    suchstring_daten = ''  
    for i in range (0,5):
      suchstring_daten= suchstring_daten + (str(ts_daten[i])) +";"

    # Benutzung von sed zum Suchen und Ersetzen in ganzen Zeilen
    # https://stackoverflow.com/questions/4427542/how-to-do-sed-like-text-replace-with-python
    # sed -i -e 's/'${pattern}'/'${repl}' "${filename}"     
    # funktioniert bis auf übrig bleibende dopplete Zeilenumbrüche:  sed -i -e 's/.*suchstring.*/ersatz/' 'datei'
    # auf Pythonisch: 
    #     kommando ="sed -i -e 's/.*{}.*/{}/' '{}'"
    #     os.system(kommando.format(suchstring,ersatz,csv_datei))
    # Doppelte Zeilenumbrüche entfernen nach https://unix.stackexchange.com/questions/76061/can-sed-remove-double-newline-characters
    #     sed -i '/^$/d' 'datei' 

    # Hier Sonderfall: Ersatz-String leer lassen: Zeile wird gelöscht, Zeilenumbruch bleibt stehen
    kommando ="sed -i -e 's/.*{}.*//' '{}'"
    os.system (kommando.format(suchstring_daten,csv_datei))

    # Doppelten Zeilenumbruch entfernen
    suchstring_zeilenumbruch = "'1!{/^$/d'}"
    kommando = "sed -i {} {}"
    os.system (kommando.format(suchstring_zeilenumbruch,csv_datei))

    # Jetzt ist Datei um den anstehenden String mit alter Payload gekürzt. Man kann die Zeile neu schreiben.

    # CSV-Datei auf der Ramdisk oeffnen, "a" steht für append, sonst wird nur eine Zeile ge- und immer wieder überschrieben
    with open(csv_datei, "a") as schreiben:   
       # Writer-Objekt erzeugen, das schreibt selbst noch nichts
       wr = csv.writer(schreiben, delimiter=';') 
       # neue Zeile schreiben  
       wr.writerow(neue_daten)

    # Werte in Datenbank schreiben
    SQL = "INSERT INTO sensorwerte (zeitstempel, node_id, child_id, command, ack, type, payload) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    try:
        data = (jetzt_postgres, ts_daten[0], ts_daten[1],ts_daten[2],ts_daten[3],ts_daten[4],ts_daten[5],)  
        cur.execute(SQL, data)
    except (Exception, psycopg2.Error) as error:
        print(error.pgerror)
    conn.commit()




	
