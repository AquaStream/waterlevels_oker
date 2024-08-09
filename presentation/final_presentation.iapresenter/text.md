# Vorhersage Wasserstände 
#### Akarshan, Oussama, Tim, Vishwa

---
# Das Problem

---
## Die Oker
---
### Die Oker
#### Zentral für Braunschweigs Geschichte und Entwicklung
	 - früher: Verteidigungsgraben um Stadtmauer
	 - heute: Naherholungsgebiet

/assets/Clipboard 8.png

Die Oker ist zentral für Braunschweigs Geschichte und Entwicklung. Früher diente sie als Verteidigungsgraben um die Stadtmauer, heute ist sie ein beliebtes Naherholungsgebiet und beliebtes Ziel für Freizeitaktivitäten wie Bootsfahrten und Spaziergänge.
---
### Die Oker
#### Überschwemmungsgefahr
	- Regenfälle
	- Hochwasser
	- Dammbruch Okertalsperre
	- besondere Bedrohung durch Klimawandel

/assets/Clipboard 9.png

Überschwemmungen der Oker stellen eine bedeutende Gefahr für Braunschweig dar. Besonders bei starken Regenfällen oder Schneeschmelze kann der Fluss schnell über die Ufer treten und angrenzende Wohngebiete gefährden

Historisch gesehen hat die Stadt immer wieder mit Hochwassern zu kämpfen gehabt, aber trotz bestehender Schutzmaßnahmen bleibt das Risiko hoch, besonders durch den Klimawandel.

---
# Die Lösung

---
## Vorhersage der Okerwasserstände

---
/assets/Clipboard.png
size: contain

---
/assets/Clipboard 1.png
size: contain

---
## Problem

---
/assets/Clipboard 2.png
size: contain
- Die Daten sind nur für das Jahr 2023 verfügbar
- Damit also viel zu wenig für einen Trainingssatz

---

/assets/Clipboard 3.png
size: contain

Stadtentwässerung Braunschweig (SE|BS)

---

/assets/Clipboard 4.png
size: contain
- Betreiber der Okertalsperre (Harzwasserwerke) stellt auch Daten bereit, aber nur der letzten 10 Tage

---
/assets/Clipboard 5.png
size: contain
- Nds. Landesbetrieb für Wasserwirtschaft, Küsten- und Naturschutz stellt ebenfalls Daten bereit, aber nur der letzten 30 Tage

---
## Also...?
---

/assets/Clipboard 7.png
size: contain

#  
	- alle drei Stellen angerufen
	- Daten von allen drei Stellen
	- Daten der letzten 12 Jahre 

Kurzerhand die jeweiligen Stellen angerufen und den Hackathon vorgestellt

von allen drei Stellen haben wir Daten über einen Zeitraum von bis zu 12 Jahren erhalten

---
# Ergebnisse

---
### Okertalsperre
/assets/okertal.png
size: contain

### Schladen
/assets/schladen.png
size: contain

### Ohrum
/assets/ohrum.png
size: contain

### Schäferbrücke
/assets/bridge.png
size: contain

### Eisenbütteler Wehr
/assets/eisenbuttel.png
size: contain

### Wendenwehr
/assets/wendwehr.png
size: contain

---
### API
/assets/Clipboard 18.png
size: contain

---
## Use Cases
	- Optimierung/Automatisierung von Wassermanagement
	- Frühzeitiges Erkennen von Bedrohungen
	- Frühzeitiges Ergreifen von Wasserschutzmaßnahmen
	- Informativ für Wassersportler:innen

---
# Methodologie

---

## Data Cleaning
---
/assets/Clipboard 10.png
size: contain
y: top

---

/assets/Clipboard 12.png
size: contain

---
## Modeling

---

/assets/Clipboard 13.png
size: contain

- karte
- Einfluss von früher auf später
- Korrelation der Wetterdaten ist unterschiedlich
- Wassermanagement an vielen Stellen

---

###### *Chain of thought* von RandomForests
/assets/Give me visualstructure how the river oker flows.png
size: contain

---

/assets/Clipboard 17.png
size: contain

## RMSE
	 - Okertalsperre: 6.97
	 - Schladen: 0.06
	 - Ohrum: 0.07
	 - Schäferbrücke: 0.1
	 - Eisenbütteler Wehr:  0.18
	 - Wendenwehr: 0.16
---
# Zukunft

---
## Zukunft
	- #### Open Data
	- #### Echtzeit Vorhersage
	- #### Vorhersage der Energieproduktion
	- #### Übertragbar in andere Städte/auf andere Flüsse
- Zugang zu Echtzeitdaten



---
# Vielen Dank
/assets/AquaStream.png
size: contain


/assets/IMG_5071.jpeg
x: right

###### Insbesondere an Laura Amelung, Sworup Basnet, Daniel Gehrmann
