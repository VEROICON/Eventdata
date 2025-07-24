# CSV → JSON-LD Konverter

Ein GUI-Tool für Windows und macOS, das CSV-Dateien mit Veranstaltungsdaten ins [Schema.org](https://schema.org/Event)-Format (JSON-LD) umwandelt.

## Features

- Automatische Trennungserkennung (Komma oder Semikolon)
- Unterstützung für deutschsprachige Feldnamen
- JSON-LD-Ausgabe im Schema.org-Format
- Plattformunabhängig (Windows & macOS)
- Benutzerfreundliches GUI mit `tkinter`

## Option 1 ohne Installation

- Trage Deine Eventdaten in die XLSX Vorlage ein (Verändere das Format nicht)
- Exportiere daraus eine CSV Datei (Codierung UTF8)
- Starte Windows_CSV_EVENTS_to_JSON.exe oder MacOS_CSV_EVENTS_to_JSON (je nach Betriebsystem - Systeme ohne Desktopumgebung --> Option 2)
- 2 Anwednungsfenster öffnen sich innerhalb von ca 5 Minuten
- wähle die als CSV (Codierung UTF8) gespeicherte Datei
- klicke konvertieren
- Ausgabe im selben Ordner als JSON-LD

## Option 2 Installation

### Voraussetzungen

- Python 3.10 oder neuer
- [Pandas](https://pandas.pydata.org/)
- Keine Adminrechte erforderlich

```bash
pip install pandas
```

## Nutzung

1. Starte das Tool:
```bash
python konverter.py
```

2. Wähle eine CSV-Datei mit korrekten Spalten (z. B. `name`, `startDate`, `location_name` etc.)
3. Das Tool erzeugt eine JSON-LD-Datei im selben Ordner.

## Beispielhafte CSV-Spalten

- `name`, `startDate`, `endDate`
- `location_name`, `location_street`, `location_city`, `location_country`
- `organizer_name`, `organizer_url`, `performer`
- `offer_price`, `offer_url`, `offer_currency`, `isAccessibleForFree`

## Lizenz

MIT License – siehe [LICENSE](LICENSE)

## Autorin

Veronika Kocher für [DIO – Data Intelligence Offensive](https://www.dataintelligence.at)
