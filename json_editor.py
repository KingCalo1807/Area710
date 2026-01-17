"""
JSON Editor für Events & Gallery - Web-basierte Version
Funktioniert auf allen Betriebssystemen ohne tkinter-Probleme
"""

import os
import json
import shutil
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import webbrowser
from threading import Timer

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Globale Variable für Projektpfad
PROJECT_PATH = os.environ.get('PROJECT_PATH', None)

# --------------------------------------
# Hilfsfunktionen
# --------------------------------------
def load_json(path):
    """Lädt JSON-Datei oder gibt leere Liste zurück"""
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Fehler beim Laden von {path}: {e}")
            return []
    return []

def save_json(path, data):
    """Speichert JSON mit Backup"""
    try:
        backup_path = path + ".backup"
        if os.path.exists(path):
            shutil.copyfile(path, backup_path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Fehler beim Speichern: {e}")
        return False

def copy_image(file, dest_folder, project_path):
    """Kopiert Bild in Zielordner und gibt relativen Pfad zurück"""
    try:
        os.makedirs(dest_folder, exist_ok=True)
        filename = secure_filename(file.filename)
        dest_path = os.path.join(dest_folder, filename)
        file.save(dest_path)

        # Relativen Pfad zum Projektordner berechnen
        rel_path = os.path.relpath(dest_path, project_path)
        return rel_path.replace("\\", "/")
    except Exception as e:
        print(f"Fehler beim Kopieren des Bildes: {e}")
        return ""

# --------------------------------------
# HTML Template
# --------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JSON Editor – Events & Gallery</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .project-selector {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .project-selector input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #007bff;
            color: white;
        }
        
        .btn-primary:hover {
            background: #0056b3;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-success:hover {
            background: #218838;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .tabs {
            display: flex;
            gap: 5px;
            border-bottom: 2px solid #ddd;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 12px 24px;
            background: #f8f9fa;
            border: none;
            cursor: pointer;
            font-size: 16px;
            border-radius: 5px 5px 0 0;
            transition: all 0.3s;
        }
        
        .tab.active {
            background: #007bff;
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .list-controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .item-list {
            list-style: none;
            border: 1px solid #ddd;
            border-radius: 5px;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        
        .item-list li {
            padding: 12px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background 0.2s;
        }
        
        .item-list li:hover {
            background: #f8f9fa;
        }
        
        .item-list li.selected {
            background: #e7f3ff;
            border-left: 3px solid #007bff;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            overflow-y: auto;
        }
        
        .modal.active {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 600px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #333;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .form-actions {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
            margin-top: 20px;
        }
        
        .alert {
            padding: 12px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .alert-success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .alert-error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>JSON Editor – Events & Gallery</h1>
        
        <div class="project-selector">
            <input type="text" id="projectPath" placeholder="Projektpfad eingeben (z.B. /Users/username/mein-projekt)" value="{{ project_path or '' }}">
            <button class="btn btn-primary" onclick="setProjectPath()">Pfad laden</button>
        </div>
        
        <div id="alert"></div>
        
        <div class="tabs">
            <button class="tab active" onclick="switchTab('events')">Events</button>
            <button class="tab" onclick="switchTab('blocked')">Private Veranstaltungen</button>
            <button class="tab" onclick="switchTab('gallery')">Gallery</button>
        </div>
        
        <!-- Events Tab -->
        <div id="events-tab" class="tab-content active">
            <div class="list-controls">
                <button class="btn btn-success" onclick="openEventModal()">Neu</button>
                <button class="btn btn-primary" onclick="editSelectedEvent()">Bearbeiten</button>
                <button class="btn btn-danger" onclick="deleteSelectedEvent()">Löschen</button>
            </div>
            <ul id="events-list" class="item-list"></ul>
        </div>
        
        <!-- Private Veranstaltungen Tab -->
        <div id="blocked-tab" class="tab-content">
            <div class="list-controls">
                <button class="btn btn-success" onclick="openBlockedModal()">Neu</button>
                <button class="btn btn-primary" onclick="editSelectedBlocked()">Bearbeiten</button>
                <button class="btn btn-danger" onclick="deleteSelectedBlocked()">Löschen</button>
            </div>
            <ul id="blocked-list" class="item-list"></ul>
        </div>
        
        <!-- Gallery Tab -->
        <div id="gallery-tab" class="tab-content">
            <div class="list-controls">
                <button class="btn btn-success" onclick="openGalleryModal()">Neu</button>
                <button class="btn btn-primary" onclick="editSelectedGallery()">Bearbeiten</button>
                <button class="btn btn-danger" onclick="deleteSelectedGallery()">Löschen</button>
            </div>
            <ul id="gallery-list" class="item-list"></ul>
        </div>
    </div>
    
    <!-- Event Modal -->
    <div id="event-modal" class="modal">
        <div class="modal-content">
            <h2 id="event-modal-title">Event bearbeiten</h2>
            <form id="event-form" onsubmit="saveEvent(event)">
                <input type="hidden" id="event-id">
                <input type="hidden" id="event-index">
                
                <div class="form-group">
                    <label>Titel (Deutsch)</label>
                    <input type="text" id="event-title-de" required>
                </div>
                
                <div class="form-group">
                    <label>Titel (English)</label>
                    <input type="text" id="event-title-en" required>
                </div>
                
                <div class="form-group">
                    <label>Beschreibung (Deutsch)</label>
                    <textarea id="event-desc-de"></textarea>
                </div>
                
                <div class="form-group">
                    <label>Beschreibung (English)</label>
                    <textarea id="event-desc-en"></textarea>
                </div>
                
                <div class="form-group">
                    <label>Kategorie</label>
                    <select id="event-category" required>
                        <option value="">Bitte wählen...</option>
                        <option value="party">Party</option>
                        <option value="workshop">Workshop</option>
                        <option value="culture">Culture</option>
                        <option value="business">Business</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Datum (YYYY-MM-DD)</label>
                    <input type="date" id="event-date">
                </div>
                
                <div class="form-group">
                    <label>Zeit (HH:MM)</label>
                    <input type="time" id="event-time">
                </div>
                
                <div class="form-group">
                    <label>Preis</label>
                    <input type="text" id="event-price">
                </div>
                
                <div class="form-group">
                    <label>Ticket URL</label>
                    <input type="url" id="event-ticket-url">
                </div>
                
                <div class="form-group">
                    <label>Bild</label>
                    <input type="file" id="event-image" accept="image/*">
                    <small id="event-current-image"></small>
                </div>
                
                <div class="form-actions">
                    <button type="button" class="btn btn-danger" onclick="closeEventModal()">Abbrechen</button>
                    <button type="submit" class="btn btn-success">Speichern</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Gallery Modal -->
    <div id="gallery-modal" class="modal">
        <div class="modal-content">
            <h2 id="gallery-modal-title">Gallery bearbeiten</h2>
            <form id="gallery-form" onsubmit="saveGallery(event)">
                <input type="hidden" id="gallery-id">
                <input type="hidden" id="gallery-index">
                
                <div class="form-group">
                    <label>Titel (Deutsch)</label>
                    <input type="text" id="gallery-title-de" required>
                </div>
                
                <div class="form-group">
                    <label>Titel (English)</label>
                    <input type="text" id="gallery-title-en" required>
                </div>
                
                <div class="form-group">
                    <label>Kategorie</label>
                    <input type="text" id="gallery-category">
                </div>
                
                <div class="form-group">
                    <label>Datum (YYYY-MM-DD)</label>
                    <input type="date" id="gallery-date">
                </div>
                
                <div class="form-group">
                    <label>Event zuordnen</label>
                    <select id="gallery-event-id">
                        <option value="">Kein Event</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Bild</label>
                    <input type="file" id="gallery-image" accept="image/*">
                    <small id="gallery-current-image"></small>
                </div>
                
                <div class="form-actions">
                    <button type="button" class="btn btn-danger" onclick="closeGalleryModal()">Abbrechen</button>
                    <button type="submit" class="btn btn-success">Speichern</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Blocked/Private Veranstaltungen Modal -->
    <div id="blocked-modal" class="modal">
        <div class="modal-content">
            <h2 id="blocked-modal-title">Private Veranstaltung bearbeiten</h2>
            <form id="blocked-form" onsubmit="saveBlocked(event)">
                <input type="hidden" id="blocked-id">
                <input type="hidden" id="blocked-index">
                
                <div class="form-group">
                    <label>Datum (YYYY-MM-DD)</label>
                    <input type="date" id="blocked-date" required>
                </div>
                
                <div class="form-group">
                    <label>Start-Zeit (HH:MM)</label>
                    <input type="time" id="blocked-start-time" required>
                </div>
                
                <div class="form-group">
                    <label>End-Zeit (HH:MM)</label>
                    <input type="time" id="blocked-end-time" required>
                </div>
                
                <div class="form-group">
                    <label>Grund / Beschreibung</label>
                    <input type="text" id="blocked-reason">
                </div>
                
                <div class="form-group">
                    <label>Status (optional)</label>
                    <select id="blocked-status">
                        <option value="">Kein Status</option>
                        <option value="reserved">Reserved</option>
                        <option value="confirmed">Confirmed</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label>Räume (optional, mehrere mit Strg/Cmd auswählen)</label>
                    <select id="blocked-rooms" multiple style="height: 100px;">
                        <option value="hall">Hall</option>
                        <option value="lab">Lab</option>
                        <option value="outdoor">Outdoor</option>
                        <option value="barclub">Bar/Club</option>
                    </select>
                    <small style="color: #666;">Keine Auswahl = alle Räume blockiert</small>
                </div>
                
                <div class="form-actions">
                    <button type="button" class="btn btn-danger" onclick="closeBlockedModal()">Abbrechen</button>
                    <button type="submit" class="btn btn-success">Speichern</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        let eventsData = [];
        let galleryData = [];
        let selectedEventIndex = null;
        let selectedGalleryIndex = null;
        let selectedBlockedIndex = null;
        
        // Tab Switching
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById(tabName + '-tab').classList.add('active');
        }
        
        // Alerts
        function showAlert(message, type = 'success') {
            const alert = document.getElementById('alert');
            alert.className = `alert alert-${type}`;
            alert.textContent = message;
            setTimeout(() => alert.textContent = '', 5000);
        }
        
        // Projektpfad setzen
        async function setProjectPath() {
            const path = document.getElementById('projectPath').value;
            if (!path) {
                showAlert('Bitte einen Pfad eingeben', 'error');
                return;
            }
            
            const response = await fetch('/set_project_path', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path})
            });
            
            const result = await response.json();
            if (result.success) {
                showAlert('Projektpfad gesetzt und Daten geladen');
                await loadData();
            } else {
                showAlert(result.error || 'Fehler beim Setzen des Pfads', 'error');
            }
        }
        
        // Daten laden
        async function loadData() {
            const response = await fetch('/get_data');
            const data = await response.json();
            
            if (data.success) {
                eventsData = data.events;
                galleryData = data.gallery;
                renderEventsList();
                renderBlockedList();
                renderGalleryList();
                populateEventDropdown();
            }
        }
        
        // Events Liste rendern
        function renderEventsList() {
            const list = document.getElementById('events-list');
            list.innerHTML = '';
            
            eventsData.forEach((event, index) => {
                if (event.type === 'event') {
                    const li = document.createElement('li');
                    li.textContent = `${event.id}: ${event.title.de}`;
                    li.onclick = () => selectEvent(index);
                    if (index === selectedEventIndex) li.classList.add('selected');
                    list.appendChild(li);
                }
            });
        }
        
        function selectEvent(index) {
            selectedEventIndex = index;
            renderEventsList();
        }
        
        // Blocked/Private Veranstaltungen Liste rendern
        function renderBlockedList() {
            const list = document.getElementById('blocked-list');
            list.innerHTML = '';
            
            eventsData.forEach((item, index) => {
                if (item.type === 'blocked') {
                    const li = document.createElement('li');
                    const reason = item.reason || 'Private Veranstaltung';
                    li.textContent = `${item.id}: ${item.date} (${item.startTime}-${item.endTime}) - ${reason}`;
                    li.onclick = () => selectBlocked(index);
                    if (index === selectedBlockedIndex) li.classList.add('selected');
                    list.appendChild(li);
                }
            });
        }
        
        function selectBlocked(index) {
            selectedBlockedIndex = index;
            renderBlockedList();
        }
        
        // Gallery Liste rendern
        function renderGalleryList() {
            const list = document.getElementById('gallery-list');
            list.innerHTML = '';
            
            galleryData.forEach((item, index) => {
                const li = document.createElement('li');
                li.textContent = `${item.id}: ${item.title.de}`;
                li.onclick = () => selectGallery(index);
                if (index === selectedGalleryIndex) li.classList.add('selected');
                list.appendChild(li);
            });
        }
        
        function selectGallery(index) {
            selectedGalleryIndex = index;
            renderGalleryList();
        }
        
        // Event Dropdown für Gallery
        function populateEventDropdown() {
            const select = document.getElementById('gallery-event-id');
            select.innerHTML = '<option value="">Kein Event</option>';
            
            eventsData.forEach(event => {
                if (event.type === 'event') {
                    const option = document.createElement('option');
                    option.value = event.id;
                    option.textContent = `${event.title.de} (${event.date})`;
                    select.appendChild(option);
                }
            });
        }
        
        // Event Modal
        function openEventModal(index = null) {
            const modal = document.getElementById('event-modal');
            const form = document.getElementById('event-form');
            form.reset();
            
            if (index !== null) {
                const event = eventsData[index];
                document.getElementById('event-modal-title').textContent = 'Event bearbeiten';
                document.getElementById('event-id').value = event.id;
                document.getElementById('event-index').value = index;
                document.getElementById('event-title-de').value = event.title.de;
                document.getElementById('event-title-en').value = event.title.en;
                document.getElementById('event-desc-de').value = event.description.de;
                document.getElementById('event-desc-en').value = event.description.en;
                document.getElementById('event-category').value = event.category;
                document.getElementById('event-date').value = event.date;
                document.getElementById('event-time').value = event.time;
                document.getElementById('event-price').value = event.price;
                document.getElementById('event-ticket-url').value = event.ticketUrl;
                document.getElementById('event-current-image').textContent = event.image ? `Aktuell: ${event.image}` : '';
            } else {
                document.getElementById('event-modal-title').textContent = 'Neues Event';
                document.getElementById('event-index').value = '';
            }
            
            modal.classList.add('active');
        }
        
        function closeEventModal() {
            document.getElementById('event-modal').classList.remove('active');
        }
        
        function editSelectedEvent() {
            if (selectedEventIndex === null) {
                showAlert('Bitte ein Event auswählen', 'error');
                return;
            }
            openEventModal(selectedEventIndex);
        }
        
        async function saveEvent(e) {
            e.preventDefault();
            
            const formData = new FormData();
            const index = document.getElementById('event-index').value;
            
            formData.append('index', index);
            formData.append('id', document.getElementById('event-id').value);
            formData.append('title_de', document.getElementById('event-title-de').value);
            formData.append('title_en', document.getElementById('event-title-en').value);
            formData.append('desc_de', document.getElementById('event-desc-de').value);
            formData.append('desc_en', document.getElementById('event-desc-en').value);
            formData.append('category', document.getElementById('event-category').value);
            formData.append('date', document.getElementById('event-date').value);
            formData.append('time', document.getElementById('event-time').value);
            formData.append('price', document.getElementById('event-price').value);
            formData.append('ticketUrl', document.getElementById('event-ticket-url').value);
            
            const imageFile = document.getElementById('event-image').files[0];
            if (imageFile) {
                formData.append('image', imageFile);
            }
            
            const response = await fetch('/save_event', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            if (result.success) {
                showAlert('Event gespeichert!');
                await loadData();
                closeEventModal();
            } else {
                showAlert(result.error || 'Fehler beim Speichern', 'error');
            }
        }
        
        async function deleteSelectedEvent() {
            if (selectedEventIndex === null) {
                showAlert('Bitte ein Event auswählen', 'error');
                return;
            }
            
            if (!confirm('Event wirklich löschen?')) return;
            
            const response = await fetch('/delete_event', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({index: selectedEventIndex})
            });
            
            const result = await response.json();
            if (result.success) {
                showAlert('Event gelöscht!');
                selectedEventIndex = null;
                await loadData();
            } else {
                showAlert(result.error || 'Fehler beim Löschen', 'error');
            }
        }
        
        // Blocked/Private Veranstaltungen Modal
        function openBlockedModal(index = null) {
            const modal = document.getElementById('blocked-modal');
            const form = document.getElementById('blocked-form');
            form.reset();
            
            if (index !== null) {
                const blocked = eventsData[index];
                document.getElementById('blocked-modal-title').textContent = 'Private Veranstaltung bearbeiten';
                document.getElementById('blocked-id').value = blocked.id;
                document.getElementById('blocked-index').value = index;
                document.getElementById('blocked-date').value = blocked.date;
                document.getElementById('blocked-start-time').value = blocked.startTime;
                document.getElementById('blocked-end-time').value = blocked.endTime;
                document.getElementById('blocked-reason').value = blocked.reason || '';
                document.getElementById('blocked-status').value = blocked.status || '';
                
                // Räume auswählen falls vorhanden
                if (blocked.room && Array.isArray(blocked.room)) {
                    const roomSelect = document.getElementById('blocked-rooms');
                    for (let option of roomSelect.options) {
                        option.selected = blocked.room.includes(option.value);
                    }
                }
            } else {
                document.getElementById('blocked-modal-title').textContent = 'Neue Private Veranstaltung';
                document.getElementById('blocked-index').value = '';
                // Standardwerte setzen
                document.getElementById('blocked-start-time').value = '00:00';
                document.getElementById('blocked-end-time').value = '23:59';
            }
            
            modal.classList.add('active');
        }
        
        function closeBlockedModal() {
            document.getElementById('blocked-modal').classList.remove('active');
        }
        
        function editSelectedBlocked() {
            if (selectedBlockedIndex === null) {
                showAlert('Bitte eine Veranstaltung auswählen', 'error');
                return;
            }
            openBlockedModal(selectedBlockedIndex);
        }
        
        async function saveBlocked(e) {
            e.preventDefault();
            
            const formData = new FormData();
            const index = document.getElementById('blocked-index').value;
            
            formData.append('index', index);
            formData.append('id', document.getElementById('blocked-id').value);
            formData.append('date', document.getElementById('blocked-date').value);
            formData.append('startTime', document.getElementById('blocked-start-time').value);
            formData.append('endTime', document.getElementById('blocked-end-time').value);
            formData.append('reason', document.getElementById('blocked-reason').value);
            formData.append('status', document.getElementById('blocked-status').value);
            
            // Räume sammeln
            const roomSelect = document.getElementById('blocked-rooms');
            const selectedRooms = Array.from(roomSelect.selectedOptions).map(opt => opt.value);
            formData.append('rooms', JSON.stringify(selectedRooms));
            
            const response = await fetch('/save_blocked', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            if (result.success) {
                showAlert('Private Veranstaltung gespeichert!');
                await loadData();
                closeBlockedModal();
            } else {
                showAlert(result.error || 'Fehler beim Speichern', 'error');
            }
        }
        
        async function deleteSelectedBlocked() {
            if (selectedBlockedIndex === null) {
                showAlert('Bitte eine Veranstaltung auswählen', 'error');
                return;
            }
            
            if (!confirm('Private Veranstaltung wirklich löschen?')) return;
            
            const response = await fetch('/delete_blocked', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({index: selectedBlockedIndex})
            });
            
            const result = await response.json();
            if (result.success) {
                showAlert('Private Veranstaltung gelöscht!');
                selectedBlockedIndex = null;
                await loadData();
            } else {
                showAlert(result.error || 'Fehler beim Löschen', 'error');
            }
        }
        
        // Gallery Modal
        function openGalleryModal(index = null) {
            const modal = document.getElementById('gallery-modal');
            const form = document.getElementById('gallery-form');
            form.reset();
            
            if (index !== null) {
                const item = galleryData[index];
                document.getElementById('gallery-modal-title').textContent = 'Gallery bearbeiten';
                document.getElementById('gallery-id').value = item.id;
                document.getElementById('gallery-index').value = index;
                document.getElementById('gallery-title-de').value = item.title.de;
                document.getElementById('gallery-title-en').value = item.title.en;
                document.getElementById('gallery-category').value = item.category;
                document.getElementById('gallery-date').value = item.date;
                document.getElementById('gallery-event-id').value = item.eventId || '';
                document.getElementById('gallery-current-image').textContent = item.image ? `Aktuell: ${item.image}` : '';
            } else {
                document.getElementById('gallery-modal-title').textContent = 'Neue Gallery';
                document.getElementById('gallery-index').value = '';
            }
            
            modal.classList.add('active');
        }
        
        function closeGalleryModal() {
            document.getElementById('gallery-modal').classList.remove('active');
        }
        
        function editSelectedGallery() {
            if (selectedGalleryIndex === null) {
                showAlert('Bitte einen Eintrag auswählen', 'error');
                return;
            }
            openGalleryModal(selectedGalleryIndex);
        }
        
        async function saveGallery(e) {
            e.preventDefault();
            
            const formData = new FormData();
            const index = document.getElementById('gallery-index').value;
            
            formData.append('index', index);
            formData.append('id', document.getElementById('gallery-id').value);
            formData.append('title_de', document.getElementById('gallery-title-de').value);
            formData.append('title_en', document.getElementById('gallery-title-en').value);
            formData.append('category', document.getElementById('gallery-category').value);
            formData.append('date', document.getElementById('gallery-date').value);
            formData.append('eventId', document.getElementById('gallery-event-id').value);
            
            const imageFile = document.getElementById('gallery-image').files[0];
            if (imageFile) {
                formData.append('image', imageFile);
            }
            
            const response = await fetch('/save_gallery', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            if (result.success) {
                showAlert('Gallery-Eintrag gespeichert!');
                await loadData();
                closeGalleryModal();
            } else {
                showAlert(result.error || 'Fehler beim Speichern', 'error');
            }
        }
        
        async function deleteSelectedGallery() {
            if (selectedGalleryIndex === null) {
                showAlert('Bitte einen Eintrag auswählen', 'error');
                return;
            }
            
            if (!confirm('Gallery-Eintrag wirklich löschen?')) return;
            
            const response = await fetch('/delete_gallery', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({index: selectedGalleryIndex})
            });
            
            const result = await response.json();
            if (result.success) {
                showAlert('Gallery-Eintrag gelöscht!');
                selectedGalleryIndex = null;
                await loadData();
            } else {
                showAlert(result.error || 'Fehler beim Löschen', 'error');
            }
        }
        
        // Initial load
        loadData();
    </script>
</body>
</html>
"""

# --------------------------------------
# Flask Routes
# --------------------------------------
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, project_path=PROJECT_PATH)

@app.route('/set_project_path', methods=['POST'])
def set_project_path():
    global PROJECT_PATH
    data = request.json
    path = data.get('path', '')

    if not path or not os.path.isdir(path):
        return jsonify({'success': False, 'error': 'Ungültiger Pfad'})

    PROJECT_PATH = path
    return jsonify({'success': True})

@app.route('/get_data')
def get_data():
    if not PROJECT_PATH:
        return jsonify({'success': False, 'error': 'Kein Projektpfad gesetzt'})

    events_path = os.path.join(PROJECT_PATH, "events.json")
    gallery_path = os.path.join(PROJECT_PATH, "gallery.json")

    events = load_json(events_path)
    gallery = load_json(gallery_path)

    return jsonify({
        'success': True,
        'events': events,
        'gallery': gallery
    })

@app.route('/save_event', methods=['POST'])
def save_event():
    if not PROJECT_PATH:
        return jsonify({'success': False, 'error': 'Kein Projektpfad gesetzt'})

    try:
        index = request.form.get('index')
        event_data = {
            'id': int(request.form.get('id')) if request.form.get('id') else None,
            'type': 'event',
            'title': {
                'de': request.form.get('title_de', ''),
                'en': request.form.get('title_en', '')
            },
            'description': {
                'de': request.form.get('desc_de', ''),
                'en': request.form.get('desc_en', '')
            },
            'category': request.form.get('category', ''),
            'date': request.form.get('date', ''),
            'time': request.form.get('time', ''),
            'price': request.form.get('price', ''),
            'ticketUrl': request.form.get('ticketUrl', ''),
            'image': ''
        }

        # Bestehendes Bild übernehmen falls vorhanden
        events_path = os.path.join(PROJECT_PATH, "events.json")
        events = load_json(events_path)
        if index and int(index) < len(events):
            event_data['image'] = events[int(index)].get('image', '')

        # Neues Bild verarbeiten
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                dest_folder = os.path.join(PROJECT_PATH, "img")
                rel_path = copy_image(file, dest_folder, PROJECT_PATH)
                if rel_path:
                    event_data['image'] = rel_path

        if index:
            # Bearbeiten
            events[int(index)] = event_data
        else:
            # Neu
            event_data['id'] = max([e.get('id', 0) for e in events] + [0]) + 1
            events.append(event_data)

        save_json(events_path, events)
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete_event', methods=['POST'])
def delete_event():
    if not PROJECT_PATH:
        return jsonify({'success': False, 'error': 'Kein Projektpfad gesetzt'})

    try:
        data = request.json
        index = data.get('index')

        events_path = os.path.join(PROJECT_PATH, "events.json")
        events = load_json(events_path)

        events.pop(index)
        save_json(events_path, events)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/save_blocked', methods=['POST'])
def save_blocked():
    if not PROJECT_PATH:
        return jsonify({'success': False, 'error': 'Kein Projektpfad gesetzt'})

    try:
        index = request.form.get('index')

        blocked_data = {
            'id': int(request.form.get('id')) if request.form.get('id') else None,
            'type': 'blocked',
            'date': request.form.get('date', ''),
            'startTime': request.form.get('startTime', ''),
            'endTime': request.form.get('endTime', '')
        }

        # Optionale Felder
        reason = request.form.get('reason', '')
        if reason:
            blocked_data['reason'] = reason

        status = request.form.get('status', '')
        if status:
            blocked_data['status'] = status

        # Räume parsen
        rooms_json = request.form.get('rooms', '[]')
        rooms = json.loads(rooms_json)
        if rooms:
            blocked_data['room'] = rooms

        events_path = os.path.join(PROJECT_PATH, "events.json")
        events = load_json(events_path)

        if index:
            # Bearbeiten
            events[int(index)] = blocked_data
        else:
            # Neu
            blocked_data['id'] = max([e.get('id', 0) for e in events] + [0]) + 1
            events.append(blocked_data)

        save_json(events_path, events)
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/delete_blocked', methods=['POST'])
def delete_blocked():
    if not PROJECT_PATH:
        return jsonify({'success': False, 'error': 'Kein Projektpfad gesetzt'})

    try:
        data = request.json
        index = data.get('index')

        events_path = os.path.join(PROJECT_PATH, "events.json")
        events = load_json(events_path)

        events.pop(index)
        save_json(events_path, events)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/save_gallery', methods=['POST'])
def save_gallery():
    if not PROJECT_PATH:
        return jsonify({'success': False, 'error': 'Kein Projektpfad gesetzt'})

    try:
        index = request.form.get('index')
        gallery_data = {
            'id': int(request.form.get('id')) if request.form.get('id') else None,
            'title': {
                'de': request.form.get('title_de', ''),
                'en': request.form.get('title_en', '')
            },
            'category': request.form.get('category', ''),
            'date': request.form.get('date', ''),
            'eventId': int(request.form.get('eventId')) if request.form.get('eventId') else None,
            'image': ''
        }

        # Bestehendes Bild übernehmen falls vorhanden
        gallery_path = os.path.join(PROJECT_PATH, "gallery.json")
        gallery = load_json(gallery_path)
        if index and int(index) < len(gallery):
            gallery_data['image'] = gallery[int(index)].get('image', '')

        # Neues Bild verarbeiten
        if 'image' in request.files:
            file = request.files['image']
            if file.filename:
                dest_folder = os.path.join(PROJECT_PATH, "gallery-images")
                rel_path = copy_image(file, dest_folder, PROJECT_PATH)
                if rel_path:
                    gallery_data['image'] = rel_path

        if index:
            # Bearbeiten
            gallery[int(index)] = gallery_data
        else:
            # Neu
            gallery_data['id'] = max([g.get('id', 0) for g in gallery] + [0]) + 1
            gallery.append(gallery_data)

        save_json(gallery_path, gallery)
        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete_gallery', methods=['POST'])
def delete_gallery():
    if not PROJECT_PATH:
        return jsonify({'success': False, 'error': 'Kein Projektpfad gesetzt'})

    try:
        data = request.json
        index = data.get('index')

        gallery_path = os.path.join(PROJECT_PATH, "gallery.json")
        gallery = load_json(gallery_path)

        gallery.pop(index)
        save_json(gallery_path, gallery)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# --------------------------------------
# Browser öffnen
# --------------------------------------
def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

# --------------------------------------
# Start
# --------------------------------------
if __name__ == '__main__':
    print("\n" + "="*50)
    print("JSON Editor startet...")
    print("Öffne Browser auf: http://127.0.0.1:5000")
    print("Zum Beenden: Strg+C drücken")
    print("="*50 + "\n")

    Timer(1, open_browser).start()
    app.run(debug=False, port=5000)