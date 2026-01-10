# 📅 EVENTS.JSON ANLEITUNG

## Übersicht
Die `events.json` Datei steuert **ALLE Events UND blockierten Tage** im Kalender.

---

## 🎉 ÖFFENTLICHE EVENTS

### Event hinzufügen:
```json
{
  "id": 1,
  "type": "event",
  "title": {
    "de": "Deutscher Titel",
    "en": "English Title"
  },
  "description": {
    "de": "Deutsche Beschreibung...",
    "en": "English description..."
  },
  "category": "party",
  "date": "2026-02-14",
  "time": "22:00",
  "price": "15€",
  "image": "img/event.jpg",
  "ticketUrl": "https://ticket.area710.de"
}
```

### Pflichtfelder:
- ✅ `id` - Eindeutige Nummer
- ✅ `type` - Muss "event" sein
- ✅ `title` - Mit DE und EN
- ✅ `description` - Mit DE und EN
- ✅ `category` - party, business, culture oder workshop
- ✅ `date` - Format: YYYY-MM-DD
- ✅ `time` - Format: HH:MM
- ✅ `price` - String (z.B. "15€" oder "Kostenlos")
- ✅ `image` - Pfad zum Bild
- ✅ `ticketUrl` - Link zum Ticket-Verkauf

### Kategorien & Farben:
- `party` → Orange (Partys, Feste)
- `business` → Rot (Business, Networking)
- `culture` → Blau (Kultur, Kunst)
- `workshop` → Grün (Workshops, Kurse)

---

## 🚫 TAGE BLOCKIEREN (Private Veranstaltungen)

### Blockierung hinzufügen:
```json
{
  "id": 3,
  "type": "blocked",
  "date": "2026-02-15",
  "reason": "Private Firmenfeier"
}
```

### Pflichtfelder:
- ✅ `id` - Eindeutige Nummer
- ✅ `type` - Muss "blocked" sein
- ✅ `date` - Format: YYYY-MM-DD
- ⚠️ `reason` - Optional (nur für interne Notizen)

### Wann blockieren?
- Private Hochzeiten
- Firmenevents (nicht öffentlich)
- Umbauarbeiten
- Feiertage (Location geschlossen)
- Bereits ausgebuchte Tage

---

## 📋 VOLLSTÄNDIGES BEISPIEL

```json
[
  {
    "id": 1,
    "type": "event",
    "title": {
      "de": "u30 Platin Party",
      "en": "u30 Platinum Party"
    },
    "description": {
      "de": "Die legendäre u30 Party ist zurück!",
      "en": "The legendary u30 party is back!"
    },
    "category": "party",
    "date": "2026-02-14",
    "time": "22:00",
    "price": "15€",
    "image": "img/dj.jpg",
    "ticketUrl": "https://ticket.area710.de"
  },
  {
    "id": 2,
    "type": "blocked",
    "date": "2026-02-15",
    "reason": "Private Hochzeit"
  },
  {
    "id": 3,
    "type": "blocked",
    "date": "2026-12-24",
    "reason": "Weihnachten - Geschlossen"
  }
]
```

---

## 🎨 IM KALENDER

### Öffentliches Event:
- Wird als **orangener Block** angezeigt
- Klickbar (Tooltip mit Titel)
- Erscheint auch in der Grid-Ansicht

### Blockierter Tag:
- Wird als **roter Block** angezeigt
- Zeigt "Ausgebucht" / "Booked"
- Erscheint NICHT in der Grid-Ansicht

### Legende:
- 🟧 Orange = Öffentliches Event
- 🟥 Rot = Private Veranstaltung / Ausgebucht
- 🟨 Gelb-Border = Heute

---

## ⚠️ WICHTIGE HINWEISE

1. **IDs müssen eindeutig sein** (keine doppelten Nummern)
2. **Datum-Format: YYYY-MM-DD** (z.B. 2026-02-14)
3. **Zeit-Format: HH:MM** (z.B. 22:00)
4. **JSON-Syntax beachten** (Kommas, Klammern!)
5. **Bilder hochladen** bevor Sie den Pfad eintragen

---

## 🔧 MEHRERE TAGE BLOCKIEREN

Für mehrere Tage einfach mehrere Einträge:

```json
[
  {
    "id": 10,
    "type": "blocked",
    "date": "2026-12-24",
    "reason": "Weihnachten"
  },
  {
    "id": 11,
    "type": "blocked",
    "date": "2026-12-25",
    "reason": "Weihnachten"
  },
  {
    "id": 12,
    "type": "blocked",
    "date": "2026-12-26",
    "reason": "Weihnachten"
  }
]
```

---

## 🚀 SCHNELL-CHECKLISTE

**Event hinzufügen:**
1. ✅ Neue ID vergeben
2. ✅ Type = "event"
3. ✅ Titel DE + EN
4. ✅ Beschreibung DE + EN
5. ✅ Kategorie wählen
6. ✅ Datum + Zeit
7. ✅ Preis + Bild + Ticket-Link

**Tag blockieren:**
1. ✅ Neue ID vergeben
2. ✅ Type = "blocked"
3. ✅ Datum
4. ✅ Grund (optional)

**Fertig!** Änderungen sind sofort sichtbar beim Neuladen der Seite.

---

## 💾 DATEI-SPEICHERORT

Die `events.json` Datei muss im gleichen Ordner wie `events.html` liegen:

```
/
├── events.html
├── events.json  ← HIER
├── img/
└── ...
```

---

## 🎉 FERTIG!

Sie können jetzt:
- ✅ Events hinzufügen/bearbeiten/löschen
- ✅ Tage für private Veranstaltungen blockieren
- ✅ Kalender automatisch aktualisieren
- ✅ Mehrsprachigkeit nutzen (DE/EN)

**Viel Erfolg!** 🚀
