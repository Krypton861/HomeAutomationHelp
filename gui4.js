// Version 4 vom 11.02.2023 mit Akkuabfrage

const jsonFilePath = 'snw.json';

//Effektiv alles was in der sensorConfig.json steht. Liste wird verwendet um snw.json Auszuwerten
const SensorNameList = [
	"TestElement_DOES NOT EXIST",
	"Thermometer",
	"Carport",
	"Kellertreppe",
	"Zisternenpegel",
	"Pumpe1Aktuell",
	"Pumpe2Aktuell",
	"Pumpe1Gespeichert",
	"Pumpe2Gespeichert",
	"Speisekammer",
	"Gästeklo",
	"Terrasse",
	"Bad 1",
	"Bad 2",
	"Schlafzimmer Matthias",
];

const SensorNameList2 = [
	["TestElement_DOES NOT EXIST","TestName"],
	["Thermometer","Thermometer"],
	["Carport","Carport"],
	["Kellertreppe","Kellertreppe"],
	["Zisternenpegel","Zisternenpegel"],
	["Pumpe1Aktuell","Pumpe1"],
	["Pumpe2Aktuell","Pumpe2"],
	["Pumpe1Gespeichert","Pumpe1G"],
	["Pumpe2Gespeichert","Pumpe2G"],
	["Speisekammer","Speisekammer"],
	["Gästeklo","Gästeklo"],
	["Terrasse","Terrasse"],
	["Bad 1","Bad 1"],
	["Bad 2","Bad 2"],
	["Schlafzimmer Matthias","Schlafzimmer Matthias"],
];

var localJsonData = {};

//Function wird ausgeführt wenn der Inhalt auf der seite erfolgreich Rendered ist.
document.addEventListener('DOMContentLoaded', function () {
	//For Data from the Server
	//fetchJsonData();

	const jsonData2 = {
		"Schlafzimmer M": {
		  "Status": {
			"Wert": "0",
			"zeitstempel": "2024-01-21 17:37:23.799616"
		  },
		  "Batterie": {
			"Wert": "100",
			"zeitstempel": "2024-01-21 17:37:24.064173"
		  }
		},
		"Bad 2": {
		  "Status": {
			"Wert": "0",
			"zeitstempel": "2024-01-21 17:21:33.241586"
		  },
		  "Batterie": {
			"Wert": "93",
			"zeitstempel": "2024-01-21 17:21:34.570072"
		  }
		},
		"Carport": {
		  "Temperatur": {
			"Wert": "0.7",
			"zeitstempel": "2024-01-21 17:42:13.056572"
		  },
		  "Batterie": {
			"Wert": "93",
			"zeitstempel": "2024-01-21 17:42:13.770163"
		  }
		},
		"Kellertreppe": {
		  "Temperatur": {
			"Wert": "1.3",
			"zeitstempel": "2024-01-21 17:42:42.815785"
		  },
		  "Batterie": {
			"Wert": "84",
			"zeitstempel": "2024-01-21 17:42:43.080348"
		  }
		},
		"Pumpe2Aktuell": {
		  "Status": {
			"Wert": "0",
			"zeitstempel": "2024-01-21 17:22:56.339723"
		  }
		},
		"Pumpe1Gespeichert": {
		  "Status": {
			"Wert": "0",
			"zeitstempel": "2024-01-21 17:22:56.569643"
		  }
		},
		"Pumpe2Gespeichert": {
		  "Status": {
			"Wert": "0",
			"zeitstempel": "2024-01-21 17:22:56.799306"
		  }
		},
		"Zisternenpegel": {
		  "Level": {
			"Wert": "99",
			"zeitstempel": "2024-01-21 17:22:57.261057"
		  }
		},
		"Speisekammer": {
		  "Status": {
			"Wert": "0",
			"zeitstempel": "2024-01-21 17:40:13.625115"
		  },
		  "Batterie": {
			"Wert": "63",
			"zeitstempel": "2024-01-21 17:40:13.889778"
		  }
		},
		"G\u00e4steklo": {
		  "Status": {
			"Wert": "0",
			"zeitstempel": "2024-01-21 17:41:40.540503"
		  },
		  "Batterie": {
			"Wert": "22",
			"zeitstempel": "2024-01-21 17:41:41.674170"
		  }
		}
	};
	
	var localSensorDataList = getSensorDataList(jsonData2);
	displaySensorData(localSensorDataList);



});

function fetchJsonData(){
	// Fetch the JSON file
	let jsonData = {};

	fetch(jsonFilePath)
		.then(response => response.json())
		.then(data => {
			// Handle the JSON data here
			jsonData = data;
			getSensorDataList(jsonData);
		})
		.catch(error => {
			console.error('Error fetching the JSON file:', error);
		});
	
}

function getSensorDataList(jsonData){
	//Input is the Raw snw.json Format. Output is a filtered List using SensorNameList. Filtering out every Element that does not exist.
	//Changed to a Object with key: "name", value: JsonData[Elem]
	var objList = [];
	SensorNameList.forEach((element) => {
		objList.push({key: element, value: jsonData[element]});
	});
	
	// Filter out undefined elements -> Does not exist in the snw.json
	var filteredList = objList.filter(function(element) {
		return element.value !== undefined;
	});
	
	//console.log(filteredList);
	return filteredList;
}

function displaySensorData(sensorDataList){
	//The Main Wrapper that is the source to all.
	var mainWrapper = document.getElementById("SensorDataWrapper");

	sensorDataList.forEach((element) => {
		//The ELement that is around the 3 Text Elems.
		var parentWrapper = document.createElement("tr"); 
		parentWrapper.classList.add("horizontalParent");

		//Create the 3 Elements With Name, Value and Battery
		/* Ist lange form von der FUnktion createChildElement
		//Left - Der NAME
		var leftElement = document.createElement("div");
		leftElement.classList.add("horizontalChild");
		leftElement.classList.add("left");

		//Center - VALUES
		var centerElement = document.createElement("div");
		centerElement.classList.add("horizontalChild");
		centerElement.classList.add("center");

		//Right
		var rightElement = document.createElement("div");
		rightElement.classList.add("horizontalChild");
		rightElement.classList.add("right");
		*/

		var leftElement = createChildElement("left");
		var centerElement = createChildElement("center");
		var rightElement = createChildElement("right");
		
		leftElement.innerHTML = element.key;

		//Zwischenspeicher, um die Farbe anhand dessen zu setzen.
		var timeDifferenceInSeconds = -1;

		if (element.value.Status !== undefined) {
			centerElement.innerHTML = element.value.Status.Wert;
			rightElement.innerHTML = getTimeDifferenceFormated(element.value.Status.zeitstempel);
			timeDifferenceInSeconds = getTimeDifferenceInMinutes(element.value.Status.zeitstempel);
		}
		else if (element.value.Level !== undefined) {
			centerElement.innerHTML = element.value.Level.Wert;
			rightElement.innerHTML = getTimeDifferenceFormated(element.value.Level.zeitstempel);
			timeDifferenceInSeconds = getTimeDifferenceInMinutes(element.value.Level.zeitstempel);
		}
		else if (element.value.Temperatur !== undefined) {
			centerElement.innerHTML = element.value.Temperatur.Wert;
			rightElement.innerHTML = getTimeDifferenceFormated(element.value.Temperatur.zeitstempel);
			timeDifferenceInSeconds = getTimeDifferenceInMinutes(element.value.Temperatur.zeitstempel);
		}		

		rightElement.style.color = "white";
		if(timeDifferenceInSeconds >= 120){
			rightElement.style.color = "red";
		}
		else if(timeDifferenceInSeconds > 60){
			rightElement.style.color = "gray";
		}
		
		
		parentWrapper.appendChild(leftElement);
		parentWrapper.appendChild(centerElement);
		parentWrapper.appendChild(rightElement);

		mainWrapper.appendChild(parentWrapper);
		//console.log(element);
	});
}

function createChildElement(className) {
	var element = document.createElement("th");
	element.classList.add("horizontalChild");
	element.classList.add(className);
	return element;
  }

function loopEverySecond() {
	setUhrzeit();

}

function getTimeDifferenceFormated(timestampString){
	//Convert string to propper timestamp
	var timestamp = new Date(timestampString);

	// Get the current time
	currentTime = new Date();

	// Calculate the time difference (in milliseconds)
	var timeDifferenceMs = currentTime - timestamp;

	//Get hour/Minute Differnece
	var hoursDifference = Math.floor(timeDifferenceMs / (1000 * 60 * 60));
	var minutesDifference = Math.floor(timeDifferenceMs / (1000 * 60) - (hoursDifference * 60)); //Bei minuten volle Stunden abziehen

	// Führende Nullen: Null links dran und dann die zwei ersten schneiden
	var hoursDifference = ('0' + hoursDifference).slice(-2); // VORSICHT !!! Wird bei einer Stunden Diff von über 100 Stunden die 10 weglassen und bei z.b. 104 -> 04 anzeigen
	var minutesDifference = ('0' + minutesDifference).slice(-2); 

	var anzeigezeit = hoursDifference + ':' + minutesDifference
	return anzeigezeit;
}


function getTimeDifferenceInMinutes(timestampString){
	//Convert string to propper timestamp
	var timestamp = new Date(timestampString);

	// Get the current time
	currentTime = new Date();

	// Calculate the time difference (in milliseconds)
	var timeDifferenceMs = currentTime - timestamp;

	//Get hour/Minute Differnece
	var minutesDifference = Math.floor(timeDifferenceMs / (1000 * 60)); //Bei minuten volle Stunden abziehen

	return minutesDifference;
}


function TestWarumUhrzeitBisherKaputtWar(){
	
	var diff5h = new Date()
	diff5h.setHours(diff5h.getHours() - 5);

	var diff3min = new Date()
	diff3min.setMinutes(diff3min.setMinutes() - 3 );

	var diffbeides = new Date()
	diffbeides.setMinutes(diffbeides.getMinutes() - 10);
	diffbeides.setHours(diffbeides.getHours() - 5);

	//Convert string to propper timestamp
	var timestamp = diff5h;
	console.log("timestamp: " + timestamp.getHours());

	// Get the current time
	currentTime = new Date();
	console.log("currentTime: " + currentTime.getHours());

	// Calculate the time difference (in milliseconds)
	var timeDifference = currentTime - timestamp;
	console.log("timeDifference raw: " + timeDifference);
	console.log("timeDifference IN Hours. Selbst Errechnet: " + timeDifference/1000/60/60);

	var timeDifference = new Date(currentTime - timestamp);
	console.log("timeDifference Date(): " + timeDifference);
	
	//Get hour/Minute Differnece
	var hoursDifference = timeDifference.getHours();
	var minutesDifference = timeDifference.getMinutes();

	// Führende Nullen: Null links dran und dann die zwei ersten schneiden
	var hoursDifference = ('0' + hoursDifference).slice(-2);
	var minutesDifference = ('0' + minutesDifference).slice(-2); 

	var anzeigezeit = hoursDifference + ':' + minutesDifference
	console.log(anzeigezeit);
}

function setUhrzeit() {
	// Uhrzeit 
	// Stunden und Minuten rausschneiden, die führende Null ergänzen,
	// Doppelpunkt dazwischen und Anzeigezeit-Variable erzeugen
	// Siehe auch: https://www.w3schools.com/jsref/met_win_setinterval.asp und andere
	jetztzeit = new Date(); // ohne var, weil global
	jetztseit1970 = jetztzeit.getTime() / 1000;  // wird auch global fürs Timeout gebraucht
	var anzeigestunden = jetztzeit.getHours();
	var anzeigeminuten = jetztzeit.getMinutes();
	var anzeigeminuten = ('0' + anzeigeminuten).slice(-2); // Führende Nullen: Null links dran und dann die zwei ersten schneiden
	var anzeigestunden = ('0' + anzeigestunden).slice(-2);
	var anzeigezeit = anzeigestunden + ':' + anzeigeminuten;

	//console.log(anzeigezeit);
	document.getElementById("UhrZeitText").innerHTML = anzeigezeit;
}



// Beautify in TextMate: Ctrl-Shift-H
function KOPF_TAB1() {
	// Hauptfunktion für Kopfzeile und MyS/Akku
	// Datei öffnen. Wenn die Konsole den Dateiinhalt ausgibt, ist alles gut
	// nach https://stackoverflow.com/questions/14446447/how-to-read-a-local-text-file, Nr. 284
	var rawFile = new XMLHttpRequest();
	rawFile.open("GET", "snw.csv", false);
	rawFile.onreadystatechange = function () { //callback funktion
		if (rawFile.readyState === 4) {
			if (rawFile.status === 200 || rawFile.status == 0) {
				var allText = rawFile.responseText;
				//alert(allText); //Die Messagebox ist zur Demonstration, allText enthält den Inhalt der *.csv-Datei
				//console.log (allText);
				result = parseCSV(allText);
				KOPF_TAB1_BEFÜLLEN(result);
			}
		}
	}
	rawFile.send(null);
}

function KOPF_TAB1_BEFÜLLEN(result) {
	// Uhrzeit 
	// Stunden und Minuten rausschneiden, die führende Null ergänzen,
	// Doppelpunkt dazwischen und Anzeigezeit-Variable erzeugen
	// Siehe auch: https://www.w3schools.com/jsref/met_win_setinterval.asp und andere
	jetztzeit = new Date(); // ohne var, weil global
	jetztseit1970 = jetztzeit.getTime() / 1000;  // wird auch global fürs Timeout gebraucht
	var anzeigestunden = jetztzeit.getHours();
	var anzeigeminuten = jetztzeit.getMinutes();
	var anzeigeminuten = ('0' + anzeigeminuten).slice(-2); // Führende Nullen: Null links dran und dann die zwei ersten schneiden
	var anzeigestunden = ('0' + anzeigestunden).slice(-2);
	var anzeigezeit = anzeigestunden + ':' + anzeigeminuten

	// Temperatur in Kopfzeile muss separat aufgerufen werden, hier muss man den Wert händisch bestimmen
	var temp_wert = temp_oben_rechts(21, 2100)[0];
	var timeout_wert = temp_oben_rechts(21, 2100)[1];
	anzeigetemperatur = '';
	var pref_1 = '<td style="text-align:right; color:white";>';
	var pref_2 = '<td style="text-align:right; color:red";>';
	var suff = '</td>';
	if (timeout_wert < 0) {
		anzeigetemperatur += pref_1;
		anzeigetemperatur += temp_wert + "°C";
		anzeigetemperatur += suff;
	}
	else {
		anzeigetemperatur += pref_2;
		anzeigetemperatur += temp_wert + "°C";
		anzeigetemperatur += suff;
	}


	// Befüllt KOPF
	// Drei Spalten
	// | Uhrzeit | Akku | Temperatur | 
	var KOPF = document.getElementById("KOPF_X");
	var aufbauen = '';
	aufbauen = '<table class="kopf">';
	aufbauen += '<colgroup>';
	aufbauen += '<col width="35%">';
	aufbauen += '<col width="30%">';
	aufbauen += '<col width="35%">';
	aufbauen += '<tr> <td style="text-align:left">' + anzeigezeit + '</td><td style="text-align:center; color:#ffffff;"; >' + fronius() + '</td>' + anzeigetemperatur;
	KOPF.innerHTML = aufbauen;


	// Befüllt TAB1
	// Fünf Spalten, ab V4a kein Piktogramm mehr
	// | Anzeigename | Wert | Timeout | Füllspalte |
	var TAB1_X = document.getElementById("TAB1_X");
	var aufbauen = '';
	aufbauen = '<table class="haupt">';
	aufbauen += '<colgroup>';
	aufbauen += '<col width="35%">';
	aufbauen += '<col width="30%">';
	aufbauen += '<col width="35%">';
	// Zeilenaufrufe mit komplettem MySensors-Datenformat
	//aufbauen += zeile ("Carport", 21, 0, 1, 0, 0, "°C", 2100, 1);
	aufbauen += zeile_mysensors("Mobil", 20, 0, 1, 0, 0, "°C", 2100, 1);
	aufbauen += zeile_mysensors("Kellertreppe", 22, 0, 1, 0, 0, "°C", 2100, 1);
	aufbauen += zeile_mysensors("Zisterne", 30, 0, 1, 0, 35, "%", 4000, 1);
	aufbauen += zeile_mysensors("Pumpe 22", 30, 1, 1, 0, 16, "läuft", 0, 0);
	aufbauen += zeile_mysensors("Pumpe 47", 30, 2, 1, 0, 16, "läuft", 0, 0);
	aufbauen += zeile_mysensors("Speisekammer", 40, 0, 1, 0, 16, "auf", 4000, 0);
	aufbauen += zeile_mysensors("Gästeklo", 41, 0, 1, 0, 16, "auf", 4000, 0);
	aufbauen += zeile_mysensors("Terrasse", 42, 0, 1, 0, 16, "auf", 4000, 0);
	aufbauen += zeile_mysensors("Bad 1", 43, 0, 1, 0, 16, "auf", 4000, 0);
	aufbauen += zeile_mysensors("Bad 2", 44, 0, 1, 0, 16, "auf", 4000, 0);
	aufbauen += zeile_mysensors("Matthias", 45, 0, 1, 0, 16, "auf", 4000, 0);
	aufbauen += '</table>';
	TAB1_X.innerHTML = aufbauen;

}

function temp_oben_rechts(nodeID, timeout) {
	// Monofunktional, nur zur Anzeige der Temperatur oben rechts
	// Das Warum erklärt sich aus der Funktion 'zeile', das hier ist eine abgespeckte Version für einen Temperaturknoten, d.h. die meisten Aufrufparameter sind bekannt.
	var temperatur = '';
	var zeitstempel = '';
	var timeout_erreicht = '';
	for (var i = 1; i < result.length; i++) {
		var feld = (result[i][0] + ";" + result[i][1] + ";" + result[i][2] + ";" + result[i][3] + ";" + result[i][4]);
		var aufruf = (nodeID + ";0;1;0;0");
		if (feld == aufruf) {
			temperatur = result[i][5]
			zeitstempel = parseFloat(result[i][6]);
			timeout_erreicht = (jetztseit1970 - zeitstempel + 3600) - timeout;
		}
	}
	return [temperatur, timeout_erreicht];
}

function zeile_mysensors(friendly_name, nodeID, childID, command, ack, type, einheit, timeout, mitWert) {
	// Struktur einer Zeile im CSV-File:    42;0;1;0;16;1;1653672462.0
	// dabei sind die Parameter NODE_ID, CHILD_ID, COMMAND, ACK, TYPE, PAYLOAD, (TIMESTAMP)
	// 'result' enthält das geparste Ergebnis von 'allText', z.B. ist im Beispiel oben result[x][0] = 42, result[x][4] = 16 usw.
	// Man kennt die Zeile nicht, in der der gesuchte Knoten im CSV-File bzw. in result steht, nur die Knotennnummer,
	// also iteriert man mit i durch, bis nodeID = result [i][0] ist

	// console.log ("Betrete Funktion, erzeugt werden soll Zeile mit " + friendly_name + " für Knoten " + nodeID);

	// Frisch anfangen.
	var zeile_ergebnis = '';
	// durch die Zeilen iterieren, bis die Größe von result erreicht ist
	for (var i = 1; i < result.length; i++) {
		// Erste vier Werte aus dem 'result' Array nehmen und zusammenfügen ergibt den Suchstring      
		var feld = (result[i][0] + ";" + result[i][1] + ";" + result[i][2] + ";" + result[i][3] + ";" + result[i][4]);
		// Selbes macht man mit dem Aufruf der Funktion
		var aufruf = (nodeID + ";" + childID + ";" + command + ";" + ack + ";" + type);
		//console.log ("Feld-String: " + feld);
		//console.log ("Aufruf-String: " + aufruf);
		// Übereinstimmung der ersten fünf Elemente bedeutet, hier stecken gesuchte Payload und Zeitstempel 
		if (feld == aufruf) {
			// console.log ("Übereinstimmung: Zähler i=" + i + "; Feldwert: " + feld + ", Aufruf: " + aufruf + " Baue Zeile auf.");  

			// Bei Übereinstimmung kann man die Zeile aufbauen
			zeile_ergebnis += '<tr>';
			// Erste Spalte: Anzeigename
			zeile_ergebnis += '<td>';
			zeile_ergebnis += friendly_name.trim();
			zeile_ergebnis += '</td>';

			// Zweite Spalte: Payload. Nur anzeigen, wenn 'mitWert' = 1 ist, sonst nur die Einheit. 
			// Damit fängt man die booleschen "tripped" Sensoren ab. Siehe auch unten, wo ggf. die ganze Zeile weggelassen wird.
			if (mitWert == 1) {
				zeile_ergebnis += '<td style="text-align:center;">';
				zeile_ergebnis += result[i][5].trim() + einheit;
				zeile_ergebnis += '</td>';
			}
			if (mitWert == 0) {
				zeile_ergebnis += '<td style="text-align:center;">';
				zeile_ergebnis += einheit;
				zeile_ergebnis += '</td>';
			}
			// Timeout berechnen und bei Überschreitung der Grenze anzeigen	(dritte Spalte)			        
			var CSVzeit = parseFloat(result[i][6]);				// Den Zeitstempel aus dem letzten Datensatz in Float wandeln
			var timediff = jetztseit1970 - CSVzeit;  			// TODO: evtl. Zeitdifferenz von 1h klären, MESZ usw.
			var timeout_formatiert;								// Hilfsvariable Zusammenbau HTML-String, der Übersichtlichkeit halber
			var timeout_ganzetage = Math.floor(timediff / 86400);
			var timeout_ganzestunden = Math.floor((timediff - (timeout_ganzetage * 86400)) / 3600);
			var timeout_ganzeminuten = Math.round((timediff - (timeout_ganzetage * 86400) - (timeout_ganzestunden * 3600)) / 60);

			// timeout_formatiert = timeout_ganzetage + "d " + timeout_ganzestunden + "h " + timeout_ganzeminuten + "'";

			if ((timediff) <= 3600) {
				timeout_formatiert = timeout_ganzeminuten + "'";
			}
			if ((timediff > 3600) && (timeout < 86400))   // 1h < Timediff < 1d
			{
				timeout_formatiert = timeout_ganzestunden + "h " + timeout_ganzeminuten + "'";
			}
			if ((timediff) >= 86400)   // Timediff >1d
			{
				timeout_formatiert = timeout_ganzetage + "d " + timeout_ganzestunden + "h " + timeout_ganzeminuten + "'";
			}

			zeile_ergebnis += '<td style="font-size: 15px; text-align: right; transform: translate(0%, 10%);">';
			zeile_ergebnis += timeout_formatiert;
			zeile_ergebnis += '</td>';



			// Wenn mitWert nicht 1 ist, will man die Zeile nur sehen, wenn Payload auch 1 ist ("tripped") und keinen Wert, sondern nur das in 'einheit' vorgegebene Statement
			if ((mitWert == 0) && (result[i][5] != 1)) { zeile_ergebnis = ''; }

		}  // vom if (feld == aufruf)
	} //for Schleife

	return zeile_ergebnis;

}

function parseCSV(allText) {
	// https://stackoverflow.com/questions/1293147/example-javascript-code-to-parse-csv-data
	// console.log ("ParseCSV betreten")
	var result = [];
	var quote = false; // 'true' means we're inside a quoted field
	// Iterate over each character, keep track of current row and column (of the returned array)
	for (var row = 0, col = 0, c = 0; c < allText.length; c++) {
		var cc = allText[c],
			nc = allText[c + 1]; // Current character, next character
		result[row] = result[row] || []; // Create a new row if necessary
		result[row][col] = result[row][col] || ''; // Create a new column (start with empty string) if necessary
		// If the current character is a quotation mark, and we're inside a
		// quoted field, and the next character is also a quotation mark,
		// add a quotation mark to the current column and skip the next character
		if (cc == '"' && quote && nc == '"') {
			result[row][col] += cc;
			++c;
			continue;
		}
		// If it's just one quotation mark, begin/end quoted field
		if (cc == '"') {
			quote = !quote;
			continue;
		}
		// If it's a comma and we're not in a quoted field, move on to the next column
		if (cc == ';' && !quote) {
			++col;
			continue;
		}
		// If it's a newline (CRLF) and we're not in a quoted field, skip the next character
		// and move on to the next row and move to column 0 of that new row
		if (cc == '\r' && nc == '\n' && !quote) {
			++row;
			col = 0;
			++c;
			continue;
		}
		// If it's a newline (LF or CR) and we're not in a quoted field,
		// move on to the next row and move to column 0 of that new row
		if (cc == '\n' && !quote) {
			++row;
			col = 0;
			continue;
		}
		if (cc == '\r' && !quote) {
			++row;
			col = 0;
			continue;
		}
		// Otherwise, append the current character to the current column
		result[row][col] += cc;
	}
	return result;
}

function temp_zu_stadt(city) {
	// entnommen aus https://forum-raspberrypi.de/forum/thread/23578-openweathermap-in-html-einbinden/
	// Daten bei https://home.openweathermap.org/
	// https://home.openweathermap.org/api_keys 
	// Mein Login: zzh67ps@funnymail.de; sawubona, die App-ID ist an das Login gebunden
	var source = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=";
	var appId = "ef148213fc71cd454ade530c7d4480b1"
	var address = source + appId;
	var json = JSON.parse(getJSON(address));
	// auf 1/10 Grad runden; math.round kann nur Ganzzahlen.
	temp = Math.round(10 * (json.main.temp - 273)) / 10 + "°C";
	return temp;
	console.log(json)
}

function fronius(param) {
	return; // Kann ich net
	// Holt den Wert von zion:8001. Dort läuft corsproxy, der diesen Aufruf an den Fronius schickt und die Antwort um den Header Access-Control-Allow-Origin ergänzt, um das CORS-Problem zu umgehen.
	// Siehe https://github.com/bulletmark/corsproxy
	var source = "http://zion:8001/solar_api/v1/GetPowerFlowRealtimeData.fcgi?Scope=Device&DeviceId=0"
	var json = JSON.parse(getJSON(source));
	var fronius_wert = json.Body.Data.Inverters[1].SOC + "%";
	fronius_wert = Math.round(parseFloat(fronius_wert) + Number.EPSILON);
	// fronius_wert = json.Head.Timestamp;  // Test
	return fronius_wert + "%";
}

function getJSON(yourUrl) {
	// entnommen aus https://forum-raspberrypi.de/forum/thread/23578-openweathermap-in-html-einbinden/
	var Httpreq = new XMLHttpRequest(); // a new request
	Httpreq.open("GET", yourUrl, false);
	Httpreq.send(null);
	return Httpreq.responseText;
}
