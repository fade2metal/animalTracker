# 🐾 Animal Tracker

Ein leichtgewichtiges, konfigurierbares RFID-Erkennungssystem für Wildtierstationen. Die Software läuft in einem Docker-Container auf einem Raspberry Pi und liest RFID-Chips von Tieren über eine WL-134-Platine aus. Erkennt Tierdurchgänge über eine Klappe und speichert die Ereignisse in einer SQLite-Datenbank. Optional wird eine Benachrichtigung per E-Mail verschickt. Eine Weboberfläche auf Basis von [NiceGUI](https://nicegui.io) ermöglicht einfache Konfiguration und Einsicht in Logs.

---

## 🔧 Hauptfunktionen

- RFID-Lesung über WL-134 Platine via UART (serial0)
- Ereignis-Erfassung (Eintritt/Austritt)
- Speicherung in SQLite-Datenbank
- Konfiguration und Visualisierung über NiceGUI Webinterface
- Optionale E-Mail-Benachrichtigungen
- Getestet auf Raspberry Pi 3B+

---

## 📷 Anwendungsszenario

Die Software dient der automatisierten Erfassung, wann ein Tier (z. B. ein Fuchs) eine Aufzuchtstation durch eine Klappe verlässt oder zurückkehrt. Beim Durchgang wird der RFID-Chip gelesen und gespeichert. Optional wird ein Alarm per E-Mail gesendet – z. B. wenn das Tier das Gelände verlässt.

---

## 📦 Projektstruktur

animalTracker/
├── AnimalTracker.py # Hauptlogik: Leseroutine, Web-UI
├── RFID.py # Dekodierung der RFID-Chips
├── db_helper.py # SQLite-Funktionen
├── setup.py # Installationsskript (optional -> Lädt beim Containerstart immer die neueste Version vom Repository)
├── requirements.txt # Python-Abhängigkeiten
└── README.md # Diese Datei


---

## 💻 Web-Oberfläche

Erstellt mit [NiceGUI](https://nicegui.io). Die Oberfläche bietet:

- Konfiguration der RFID-Ereignisse
- Einsicht in aktuelle und historische Ereignisse
- Verwaltung der bekannten RFID-Tags
- Einstellungen für Mailversand und Systemverhalten

Nach dem Start erreichbar unter:  
`http://<RPI-IP>:8080`

---

## ⚙️ Hardware / GPIO-Belegung

Der WL-134 Reader wird über UART (serial0) mit dem Raspberry Pi verbunden.

### 📌 Pin-Belegung Raspberry Pi zu WL-134:

Raspberry Pi Pin  | WL-134 Anschluss |
----------------- | ---------------- |
GPIO15 (RXD)      | 3.3vTX           |
GND               | GND              |
5V (Pin 2 oder 4) | +5-9V            |


📝 Hinweis:  
Die serielle Konsole muss deaktiviert und UART aktiviert sein:

```bash
sudo raspi-config
# → Schnittstellenoptionen → Seriell → Login-Shell: Nein, Serielle Schnittstelle: Ja
🐳 Docker Setup

Voraussetzungen

Raspberry Pi OS
Docker & Docker Compose
serial0 aktiv & verfügbar

Dockerfile (Ausschnitt)
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "AnimalTracker.py"]

docker-compose.yml (Beispiel)
version: '3'
services:
  animaltracker:
    build: .
    restart: unless-stopped
    ports:
      - "8080:8080"
    devices:
      - "/dev/serial0:/dev/serial0"
    volumes:
      - ./data:/app/data

Start:

docker-compose up --build -d
🛠 Konfiguration

Die Konfigurationsdaten (Mailserver, Tagnamen etc.) sind über die NiceGUI-Weboberfläche einstellbar. Änderungen werden automatisch in der SQLite-Datenbank gespeichert.

🗃️ Datenbank (SQLite)

Die App erzeugt automatisch eine rfid.db mit folgenden Tabellen (Beispielstruktur):

events – Protokolliert RFID-Events mit Timestamp
tags – Bekannte RFID-Tags
settings – Konfiguration (z. B. Mailserver, Alarmverhalten)

📬 E-Mail-Benachrichtigung (optional)

Wenn aktiviert, wird bei definierten Ereignissen (z. B. Verlassen der Station) eine E-Mail versendet. Die SMTP-Daten sind über das Webinterface einstellbar.

🚧 Roadmap / Ideen

Benutzerauthentifizierung im Webinterface
Whitelisting/Blacklisting von Tags
Exportfunktionen (CSV, PDF)
Tierindividuelle Statusanzeigen (z. B. “seit X Tagen nicht erkannt”)
SMS/Push-Integration (z. B. über Signal oder Pushover)
🐾 Lizenz 

MIT License.