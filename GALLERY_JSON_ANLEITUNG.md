# 📸 GALLERY.JSON ANLEITUNG - MIT SUCHFUNKTION & EVENT-VERKNÜPFUNG

## 🆕 NEUE FEATURES!

### 1. 🔍 SUCHFUNKTION
- Durchsucht **Titel**, **Kategorie** UND **Event-Namen**
- Live-Suche (sucht während dem Tippen)
- Kombinierbar mit Filtern
- Übersetzbar (DE/EN)

### 2. 🔗 EVENT-VERKNÜPFUNG
- Verknüpfe Galerie-Bilder mit Events aus dem Kalender
- Event-Name wird im Bild-Overlay angezeigt
- Klickbarer Link zum Event
- Durchsuchbar nach Event-Name

---

## 📋 BILD-STRUKTUR

### Basis-Struktur (wie vorher):
```json
{
  "id": 1,
  "title": {
    "de": "Deutscher Titel",
    "en": "English Title"
  },
  "category": "party",
  "date": "14.02.2025",
  "image": "gallery-images/bild-name.jpg"
}
```

### 🆕 NEU: Mit Event-Verknüpfung:
```json
{
  "id": 1,
  "title": {
    "de": "u30 Platin Party 2025",
    "en": "u30 Platinum Party 2025"
  },
  "category": "party",
  "date": "14.02.2025",
  "image": "gallery-images/u30-party-1.jpg",
  "eventId": 1
}
```

**NEU: `eventId` Feld (optional)**
- Verknüpft das Bild mit einem Event aus `events.json`
- Muss mit der `id` eines Events übereinstimmen
- Ist **OPTIONAL** - kann weggelassen werden

---

## 🔗 EVENT-VERKNÜPFUNG: SO FUNKTIONIERT'S

### Schritt 1: Event-ID finden

Öffne `events.json` und finde die ID deines Events:

```json
{
  "id": 1,
  "type": "event",
  "title": {
    "de": "u30 Platin Party",
    "en": "u30 Platinum Party"
  },
  ...
}
```

→ Event-ID ist: **1**

### Schritt 2: ID in Gallery eintragen

Füge das `eventId` Feld zum Galerie-Bild hinzu:

```json
{
  "id": 13,
  "title": {
    "de": "Party Crowd u30",
    "en": "Party Crowd u30"
  },
  "category": "party",
  "date": "14.02.2025",
  "image": "gallery-images/party-crowd-1.jpg",
  "eventId": 1  ← Event-ID hier eintragen
}
```

### Was passiert dann?

✅ **Im Bild-Overlay:**
- Event-Name wird als Tag angezeigt
- Beispiel: "📅 u30 Platin Party"

✅ **In der Lightbox:**
- Klickbarer Link: "📅 Zum Event: u30 Platin Party"
- Führt direkt zur Events-Seite

✅ **In der Suche:**
- Du kannst nach dem Event-Namen suchen
- Beispiel: Suche "u30" findet alle Bilder vom u30 Event

---

## 🔍 SUCHFUNKTION NUTZEN

### Live-Suche:
```
Eingabe: "party"
→ Findet: Alle Bilder mit "party" in Titel oder Kategorie

Eingabe: "u30"
→ Findet: Alle Bilder vom u30 Event

Eingabe: "halloween"
→ Findet: Halloween-Bilder und verknüpfte Events
```

### Kombiniert mit Filtern:
1. Filter auf "Party" klicken
2. In Suchfeld "u30" eingeben
→ Zeigt nur Party-Bilder vom u30 Event

---

## 📊 VOLLSTÄNDIGES BEISPIEL

```json
[
  {
    "id": 1,
    "title": {
      "de": "u30 Party Eingang",
      "en": "u30 Party Entrance"
    },
    "category": "party",
    "date": "14.02.2025",
    "image": "gallery-images/u30-entrance.jpg",
    "eventId": 1
  },
  {
    "id": 2,
    "title": {
      "de": "u30 Tanzfläche",
      "en": "u30 Dance Floor"
    },
    "category": "party",
    "date": "14.02.2025",
    "image": "gallery-images/u30-dancefloor.jpg",
    "eventId": 1
  },
  {
    "id": 3,
    "title": {
      "de": "Hall Setup",
      "en": "Hall Setup"
    },
    "category": "location",
    "date": "10.01.2026",
    "image": "gallery-images/hall-1.jpg"
  }
]
```

**Beachte:**
- Bild 1 & 2: Mit Event verknüpft (`eventId: 1`)
- Bild 3: OHNE Event-Verknüpfung (kein `eventId` Feld)

---

## 🚀 SCHRITT-FÜR-SCHRITT: EVENT-VERKNÜPFUNG

### 1. Event in events.json prüfen:
```json
// In events.json:
{
  "id": 7,
  "type": "event",
  "title": {
    "de": "Halloween Horror Night",
    "en": "Halloween Horror Night"
  },
  ...
}
```

### 2. Bilder vom Event hochladen:
- `gallery-images/halloween-crowd.jpg`
- `gallery-images/halloween-deco.jpg`
- `gallery-images/halloween-dj.jpg`

### 3. In gallery.json eintragen:
```json
{
  "id": 20,
  "title": {
    "de": "Halloween Crowd",
    "en": "Halloween Crowd"
  },
  "category": "party",
  "date": "31.10.2025",
  "image": "gallery-images/halloween-crowd.jpg",
  "eventId": 7  ← Event-ID von Halloween
},
{
  "id": 21,
  "title": {
    "de": "Halloween Dekoration",
    "en": "Halloween Decoration"
  },
  "category": "events",
  "date": "31.10.2025",
  "image": "gallery-images/halloween-deco.jpg",
  "eventId": 7
}
```

### 4. Fertig!
- Beide Bilder zeigen "📅 Halloween Horror Night"
- Suche nach "halloween" findet beide
- Link führt zum Event im Kalender

---

## 💡 BEST PRACTICES

### Event-Verknüpfung sinnvoll nutzen:

✅ **VERKNÜPFE:**
- Fotos von spezifischen Events
- Party-Impressionen
- Event-Atmosphäre
- Publikum bei Events

❌ **NICHT VERKNÜPFEN:**
- Allgemeine Location-Fotos
- Standard-Ausstattung
- Räume ohne Event
- Beispiel-Setups

### Kategorien richtig wählen:

**events** → Fotos von öffentlichen Events  
**party** → Party-Atmosphäre & Crowd  
**business** → Business-Events & Konferenzen  
**location** → Räume, Ausstattung, Setup

---

## 🔄 MEHRERE BILDER EINEM EVENT ZUORDNEN

Beispiel: 5 Bilder vom gleichen Event

```json
[
  {
    "id": 10,
    "title": {"de": "Sommerfest Eingang", "en": "Summer Festival Entrance"},
    "category": "events",
    "date": "20.06.2025",
    "image": "gallery-images/sommerfest-entrance.jpg",
    "eventId": 6
  },
  {
    "id": 11,
    "title": {"de": "Sommerfest Bühne", "en": "Summer Festival Stage"},
    "category": "events",
    "date": "20.06.2025",
    "image": "gallery-images/sommerfest-stage.jpg",
    "eventId": 6
  },
  {
    "id": 12,
    "title": {"de": "Sommerfest Crowd", "en": "Summer Festival Crowd"},
    "category": "party",
    "date": "20.06.2025",
    "image": "gallery-images/sommerfest-crowd.jpg",
    "eventId": 6
  },
  {
    "id": 13,
    "title": {"de": "Sommerfest Catering", "en": "Summer Festival Catering"},
    "category": "business",
    "date": "20.06.2025",
    "image": "gallery-images/sommerfest-catering.jpg",
    "eventId": 6
  },
  {
    "id": 14,
    "title": {"de": "Sommerfest Outdoor", "en": "Summer Festival Outdoor"},
    "category": "location",
    "date": "20.06.2025",
    "image": "gallery-images/sommerfest-outdoor.jpg",
    "eventId": 6
  }
]
```

**Alle 5 Bilder:**
- Haben die gleiche `eventId: 6`
- Zeigen "📅 Sommerfest 2025"
- Sind über Suche "Sommerfest" findbar
- Können verschiedene Kategorien haben

---

## 🆚 MIT vs. OHNE Event-Verknüpfung

### MIT eventId:
```json
{
  "id": 1,
  "title": {"de": "u30 Party", "en": "u30 Party"},
  "category": "party",
  "date": "14.02.2025",
  "image": "gallery-images/u30-1.jpg",
  "eventId": 1  ← MIT Verknüpfung
}
```

**Ergebnis:**
- ✅ Event-Tag im Overlay
- ✅ Link zum Event
- ✅ Suchbar nach Event-Name
- ✅ Zeigt: "📅 u30 Platin Party"

### OHNE eventId:
```json
{
  "id": 2,
  "title": {"de": "Hall Setup", "en": "Hall Setup"},
  "category": "location",
  "date": "10.01.2026",
  "image": "gallery-images/hall-1.jpg"
}
```

**Ergebnis:**
- ✅ Normales Galerie-Bild
- ❌ Kein Event-Tag
- ❌ Kein Link
- ✅ Trotzdem suchbar nach Titel

---

## 🎯 ANWENDUNGSBEISPIELE

### Szenario 1: u30 Party
```
Event in events.json: id: 1, "u30 Platin Party"
Galerie-Bilder:
- u30-entrance.jpg (eventId: 1)
- u30-dancefloor.jpg (eventId: 1)
- u30-crowd.jpg (eventId: 1)
- u30-bar.jpg (eventId: 1)

→ User sucht "u30" → findet alle 4 Bilder
→ User klickt Bild → sieht Event-Link
```

### Szenario 2: Allgemeine Fotos
```
Location-Bilder OHNE Event:
- hall-empty.jpg (keine eventId)
- outdoor-day.jpg (keine eventId)
- lab-setup.jpg (keine eventId)

→ Zeigen nur Location
→ Kein Event-Link
→ Trotzdem filterbar & suchbar
```

---

## 📱 FEATURES IM ÜBERBLICK

### ✅ Suchfunktion:
- Live-Suche
- Durchsucht: Titel, Kategorie, Event-Name
- Kombinierbar mit Filtern
- Übersetzbar (DE/EN)

### ✅ Event-Verknüpfung:
- Optional mit `eventId`
- Event-Name als Tag
- Link zum Event
- Durchsuchbar

### ✅ Filter:
- Alle Bilder
- Events
- Location
- Party
- Business

### ✅ Lightbox:
- Großansicht
- Event-Link (falls vorhanden)
- Navigation (Vor/Zurück)
- Keyboard (Pfeiltasten, ESC)

---

## 🔧 TROUBLESHOOTING

### Problem: Event-Link wird nicht angezeigt
✅ **Prüfen:**
1. Ist `eventId` im Galerie-Bild vorhanden?
2. Existiert Event mit dieser ID in `events.json`?
3. Ist Event-Type = "event" (nicht "blocked")?

### Problem: Suche findet Event nicht
✅ **Prüfen:**
1. Ist `eventId` korrekt eingetragen?
2. Stimmt die ID mit `events.json` überein?
3. Cache leeren & Seite neu laden

### Problem: Falscher Event-Name
✅ **Prüfen:**
1. Event-ID in beiden Dateien gleich?
2. Tippfehler in der ID?
3. events.json aktualisiert?

---

## 💾 DATEI-ANFORDERUNGEN

```
Root/
├── gallery.html  (oder gallery-COMPLETE.html)
├── gallery.json  (mit optionalen eventId Feldern)
├── events.json   (wird automatisch geladen)
└── gallery-images/
    ├── bild-1.jpg
    ├── bild-2.jpg
    └── ...
```

**Wichtig:**
- `events.json` muss im gleichen Verzeichnis sein
- Event-IDs müssen übereinstimmen
- Events mit `type: "blocked"` werden NICHT verknüpft

---

## 🎊 CHECKLISTE

**Bild mit Event-Verknüpfung hinzufügen:**
- [ ] Event-ID in `events.json` gefunden
- [ ] Bild in `gallery-images/` hochgeladen
- [ ] Neuen Eintrag in `gallery.json` erstellt
- [ ] `eventId` Feld hinzugefügt
- [ ] ID, Titel, Kategorie, Datum ausgefüllt
- [ ] Datei gespeichert
- [ ] Seite neu geladen
- [ ] Event-Tag wird angezeigt
- [ ] Link funktioniert
- [ ] Suche findet Bild

**Bild OHNE Event-Verknüpfung:**
- [ ] Bild hochgeladen
- [ ] Eintrag in `gallery.json`
- [ ] `eventId` NICHT hinzufügen
- [ ] Speichern & Testen

---

## 🎨 BEISPIEL-WORKFLOW

### Neues Event fotografiert:

1. **Event prüfen:**
   - `events.json` öffnen
   - Event-ID notieren (z.B. `id: 5`)

2. **Fotos hochladen:**
   - 10 Fotos → `gallery-images/`

3. **In gallery.json eintragen:**
   ```json
   {
     "id": 50,
     "title": {"de": "Event Foto 1", "en": "Event Photo 1"},
     "category": "party",
     "date": "15.03.2026",
     "image": "gallery-images/event-photo-1.jpg",
     "eventId": 5
   },
   // ... 9 weitere Bilder ...
   ```

4. **Testen:**
   - Seite laden
   - Nach Event-Name suchen
   - Event-Link klicken

5. **Fertig!** 🎉

---

## 📞 SUPPORT

Bei Fragen:
- E-Mail: info@area710.de
- Telefon: +49 7031 41073-11

**Viel Erfolg mit der neuen Galerie!** 📸🔍✨
