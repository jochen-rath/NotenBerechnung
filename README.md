# NotenBerechnung
Diese Datei berechnet die Noten, die mit der App SitzplanNoteneingabe gesetzt werden.

## Beschreibung
Diese App berechnet die durschnittswerte der mündlichen Noten, die mit der App SitzplanNoteneingabe erzeugt werden. Dadurch kann man Schülern einen Zwischenstand der aktuellen mündlichen Noten geben.


## Voraussetzungen
Die App ist in Python geschrieben und benötigt Kivy. Installiere es mit
```
pip3 install kivy
```

## Android App erstellen
In der Datei buildozer.spec sind die Voraussetzungen zur Erzeugung der Android App gegeben. Erzeuge die App mit dem Befehl
```
buildozer android debug
```

## Nutzung
Auf einem Linux/Windows Computer kann die App direkt genutzt werden:
```
python main.py
```
Der Ziel ist es aber, die App auf einem Android Smartphone zu nutzen.

 1. Erstelle im Home-Verzeichnis den Ordner "sitzplanNoten".
 2. Die App greift auf dem Pfad "os.path.join(os.getenv('EXTERNAL_STORAGE'),'sitzplanNoten')" zu.
 3. Installiere die App auf deinem Gerät
 4. Gib der App die Berechtigung, auf den Externen-Speicher zuzugreifen. Dies wird noch nicht abgefragt.
 5. Erstelle mündliche Noten mit der App SitzplanNoteneingabe.
 6. Lass dir die durchschnittsnoten anzeigen.

