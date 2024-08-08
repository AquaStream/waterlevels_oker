# Vorhersage Wasserstände 
#### Akarshan, Oussama, Tim, Vishwa

---
# Das Problem

---
## Die Oker
---
### Die Oker
#### Zentral für Braunschweigs Geschichte und Entwicklung
	 - früher: Verteidigungsgraben und Stadtmauer
	 - heute: Naherholungsgebiet

Die Oker ist zentral für Braunschweigs Geschichte und Entwicklung. Früher diente sie als Verteidigungsgraben um die Stadtmauer, heute ist sie ein beliebtes Naherholungsgebiet und beliebtes Ziel für Freizeitaktivitäten wie Bootsfahrten und Spaziergänge.
---
### Die Oker
#### Überschwemmungsgefahr
	- Regenfälle
	- Hochwasser
	- Dammbruch Okertalsperre
	- besondere Bedrohung durch Klimawandel

Überschwemmungen der Oker stellen eine bedeutende Gefahr für Braunschweig dar. Besonders bei starken Regenfällen oder Schneeschmelze kann der Fluss schnell über die Ufer treten und angrenzende Wohngebiete gefährden

Historisch gesehen hat die Stadt immer wieder mit Hochwassern zu kämpfen gehabt, aber trotz bestehender Schutzmaßnahmen bleibt das Risiko hoch, besonders durch den Klimawandel.

---
# Die Lösung

---
## Vorhersage der Okerwasserstände

---
/assets/Clipboard.png
background: true

---
/assets/Clipboard 1.png

---
## Problem

---
/assets/Clipboard 2.png
- Die Daten sind nur für das Jahr 2023 verfügbar
- Damit also viel zu wenig für einen Trainingssatz

---

/assets/Clipboard 3.png

Stadtentwässerung Braunschweig (SE|BS)

---

/assets/Clipboard 4.png
- Betreiber der Okertalsperre (Harzwasserwerke) stellt auch Daten bereit, aber nur der letzten 10 Tage

---
/assets/Clipboard 5.png
- Nds. Landesbetrieb für Wasserwirtschaft, Küsten- und Naturschutz stellt ebenfalls Daten bereit, aber nur der letzten 30 Tage

---
## Also...?
---

/assets/Clipboard 7.png
size: contain

	- alle drei Stellen angerufen
	- Daten von allen drei Stellen
	- Daten der letzten 12 Jahre 

Kurzerhand die jeweiligen Stellen angerufen und den Hackathon vorgestellt

von allen drei Stellen haben wir Daten über einen Zeitraum von bis zu 12 Jahren erhalten

---
# Methodologie

---
## Methodologie
### Chain von RandomForests
	- Vorhersage des Wasserstands der Okertalsperre mit Hilfe von Wetterdaten des Deutschen Wetterdienst über API 
	- Vorhersage in Schladen 
	- 	Vorhersage in Ohrum 
	- Vorhersage an der Schäferbrücke
	- Vorhersage am Eisenbütteler Wehr 
	- Vorhersage am Wendenwehr
### Metrics
	- RMSE von XXX
	- MAE von XXX

---
# Ergebnisse

---
## Ergebnisse


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
###### Insbesondere an Laura Amelung, Sworup Basnet, Daniel Gehrmann