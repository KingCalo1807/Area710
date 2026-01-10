<?php
/**
 * area710 Booking Handler
 * Verarbeitet Buchungsanfragen und sendet E-Mails
 */

// Error Reporting für Entwicklung (auf Produktion ausschalten!)
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);

// CORS Headers (anpassen für Produktion!)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json; charset=utf-8');

// Handle OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Nur POST erlauben
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
    exit();
}

// ========================================
// KONFIGURATION
// ========================================

// E-Mail-Empfänger (area710) //TO-DO: Anpassen
define('RECIPIENT_EMAIL', 'info@area710.de');
define('RECIPIENT_NAME', 'area710 Eventbüro');

// Absender (sollte eine eigene Domain-E-Mail sein!)
define('SENDER_EMAIL', 'noreply@area710.de'); //TO-DO: Anpassen wenn weiterleitung nicht geht, dann: Beim Hoster ins E-Mail-Menü: noreply@area710.de → info@area710.de
define('SENDER_NAME', 'area710 Buchungssystem');

// BCC Kopie (optional)
define('BCC_EMAIL', ''); // Leer lassen wenn nicht benötigt

// ========================================
// DATEN EMPFANGEN
// ========================================

$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    http_response_code(400);
    echo json_encode(['success' => false, 'message' => 'Invalid JSON']);
    exit();
}

// ========================================
// VALIDIERUNG
// ========================================

$errors = [];

// Pflichtfelder prüfen
$required = ['firstName', 'lastName', 'email', 'phone', 'eventType', 'eventDate', 'eventTime', 'duration', 'guests'];
foreach ($required as $field) {
    if (empty($data[$field])) {
        $errors[] = "Feld '$field' ist erforderlich";
    }
}

// E-Mail validieren
if (!empty($data['email']) && !filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Ungültige E-Mail-Adresse';
}

// Datum validieren
if (!empty($data['eventDate'])) {
    $eventDate = strtotime($data['eventDate']);
    if ($eventDate < strtotime('today')) {
        $errors[] = 'Datum muss in der Zukunft liegen';
    }
}

// Fehler zurückgeben
if (!empty($errors)) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'message' => implode(', ', $errors)
    ]);
    exit();
}

// ========================================
// DATEN VORBEREITEN
// ========================================

$firstName = htmlspecialchars($data['firstName']);
$lastName = htmlspecialchars($data['lastName']);
$email = htmlspecialchars($data['email']);
$phone = htmlspecialchars($data['phone']);
$company = htmlspecialchars($data['company'] ?? '');
$eventType = htmlspecialchars($data['eventType']);
$eventDate = htmlspecialchars($data['eventDate']);
$eventTime = htmlspecialchars($data['eventTime']);
$duration = htmlspecialchars($data['duration']);
$guests = htmlspecialchars($data['guests']);
$message = htmlspecialchars($data['message'] ?? '');
$lang = htmlspecialchars($data['lang'] ?? 'de');

// Räume
$rooms = isset($data['rooms']) && is_array($data['rooms']) ? $data['rooms'] : [];
$roomsText = !empty($rooms) ? implode(', ', array_map('htmlspecialchars', $rooms)) : 'Keine Auswahl';

// Services
$services = isset($data['services']) && is_array($data['services']) ? $data['services'] : [];
$servicesText = !empty($services) ? implode(', ', array_map('htmlspecialchars', $services)) : 'Keine Auswahl';

// Event-Typ übersetzen
$eventTypes = [
    'business' => ['de' => 'Business Event', 'en' => 'Business Event'],
    'wedding' => ['de' => 'Hochzeit', 'en' => 'Wedding'],
    'birthday' => ['de' => 'Geburtstag', 'en' => 'Birthday'],
    'party' => ['de' => 'Party', 'en' => 'Party'],
    'conference' => ['de' => 'Konferenz/Tagung', 'en' => 'Conference/Meeting'],
    'workshop' => ['de' => 'Workshop/Seminar', 'en' => 'Workshop/Seminar'],
    'other' => ['de' => 'Sonstiges', 'en' => 'Other']
];
$eventTypeLabel = isset($eventTypes[$eventType]) ? $eventTypes[$eventType][$lang] : $eventType;

// ========================================
// E-MAIL AN AREA710 (Owner Notification)
// ========================================

$subject_owner = "Neue Buchungsanfrage von $firstName $lastName";

$message_owner = "
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #FCAB14, #CD1151); color: white; padding: 30px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; }
        .section { margin-bottom: 25px; }
        .section h3 { color: #FCAB14; border-bottom: 2px solid #FCAB14; padding-bottom: 5px; margin-bottom: 15px; }
        .info-row { display: flex; margin-bottom: 10px; }
        .label { font-weight: bold; min-width: 180px; color: #666; }
        .value { color: #333; }
        .footer { text-align: center; padding: 20px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>Neue Buchungsanfrage</h1>
            <p>area710 - UNIQUE EVENT LOCATION</p>
        </div>
        
        <div class='content'>
            <div class='section'>
                <h3>Kontaktdaten</h3>
                <div class='info-row'><span class='label'>Name:</span><span class='value'>$firstName $lastName</span></div>
                " . ($company ? "<div class='info-row'><span class='label'>Firma:</span><span class='value'>$company</span></div>" : "") . "
                <div class='info-row'><span class='label'>E-Mail:</span><span class='value'><a href='mailto:$email'>$email</a></span></div>
                <div class='info-row'><span class='label'>Telefon:</span><span class='value'><a href='tel:$phone'>$phone</a></span></div>
            </div>
            
            <div class='section'>
                <h3>Event-Details</h3>
                <div class='info-row'><span class='label'>Art der Veranstaltung:</span><span class='value'>$eventTypeLabel</span></div>
                <div class='info-row'><span class='label'>Datum:</span><span class='value'>$eventDate</span></div>
                <div class='info-row'><span class='label'>Uhrzeit:</span><span class='value'>$eventTime Uhr</span></div>
                <div class='info-row'><span class='label'>Dauer:</span><span class='value'>$duration Stunden</span></div>
                <div class='info-row'><span class='label'>Anzahl Gäste:</span><span class='value'>$guests Personen</span></div>
            </div>
            
            <div class='section'>
                <h3>Raumauswahl</h3>
                <div class='info-row'><span class='label'>Gewünschte Räume:</span><span class='value'>$roomsText</span></div>
            </div>
            
            " . (!empty($services) ? "
            <div class='section'>
                <h3>Zusätzliche Services</h3>
                <div class='info-row'><span class='label'>Gewählte Services:</span><span class='value'>$servicesText</span></div>
            </div>
            " : "") . "
            
            " . ($message ? "
            <div class='section'>
                <h3>Nachricht</h3>
                <p>" . nl2br($message) . "</p>
            </div>
            " : "") . "
        </div>
        
        <div class='footer'>
            <p>Diese Anfrage wurde über das Buchungsformular auf area710.de gesendet.</p>
            <p>Bitte antworten Sie dem Kunden zeitnah.</p>
        </div>
    </div>
</body>
</html>
";

$headers_owner = "MIME-Version: 1.0" . "\r\n";
$headers_owner .= "Content-type:text/html;charset=UTF-8" . "\r\n";
$headers_owner .= "From: " . SENDER_NAME . " <" . SENDER_EMAIL . ">" . "\r\n";
$headers_owner .= "Reply-To: $firstName $lastName <$email>" . "\r\n";
if (BCC_EMAIL) {
    $headers_owner .= "Bcc: " . BCC_EMAIL . "\r\n";
}

$mail_owner_sent = mail(RECIPIENT_EMAIL, $subject_owner, $message_owner, $headers_owner);

// ========================================
// BESTÄTIGUNGS-E-MAIL AN KUNDEN
// ========================================

$subject_customer = $lang === 'de' 
    ? "Ihre Buchungsanfrage bei area710" 
    : "Your booking request at area710";

$greeting = $lang === 'de' 
    ? "Vielen Dank für Ihre Buchungsanfrage!" 
    : "Thank you for your booking request!";

$intro = $lang === 'de'
    ? "Wir haben Ihre Anfrage erhalten und werden uns innerhalb von 24 Stunden bei Ihnen melden."
    : "We have received your request and will contact you within 24 hours.";

$summary_title = $lang === 'de' ? "Zusammenfassung Ihrer Anfrage:" : "Summary of your request:";
$contact_title = $lang === 'de' ? "Ihre Kontaktdaten:" : "Your contact details:";
$event_title = $lang === 'de' ? "Event-Details:" : "Event details:";
$rooms_title = $lang === 'de' ? "Gewählte Räume:" : "Selected rooms:";
$services_title = $lang === 'de' ? "Zusätzliche Services:" : "Additional services:";
$message_title = $lang === 'de' ? "Ihre Nachricht:" : "Your message:";
$questions = $lang === 'de'
    ? "Bei Fragen erreichen Sie uns unter:"
    : "If you have any questions, please contact us:";

$message_customer = "
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #FCAB14, #CD1151); color: white; padding: 30px; text-align: center; }
        .content { background: #f9f9f9; padding: 30px; }
        .section { margin-bottom: 20px; }
        .section h3 { color: #FCAB14; margin-bottom: 10px; }
        .info-row { margin-bottom: 8px; }
        .label { font-weight: bold; color: #666; }
        .contact-box { background: white; padding: 20px; border-left: 4px solid #FCAB14; margin-top: 20px; }
        .footer { text-align: center; padding: 20px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>$greeting</h1>
            <p>area710 - UNIQUE EVENT LOCATION</p>
        </div>
        
        <div class='content'>
            <p>Hallo $firstName $lastName,</p>
            <p>$intro</p>
            
            <h3>$summary_title</h3>
            
            <div class='section'>
                <p><span class='label'>$event_title</span></p>
                <div class='info-row'>$eventTypeLabel am $eventDate um $eventTime Uhr</div>
                <div class='info-row'>$duration Stunden | $guests Gäste</div>
            </div>
            
            <div class='section'>
                <p><span class='label'>$rooms_title</span></p>
                <div class='info-row'>$roomsText</div>
            </div>
            
            " . (!empty($services) ? "
            <div class='section'>
                <p><span class='label'>$services_title</span></p>
                <div class='info-row'>$servicesText</div>
            </div>
            " : "") . "
            
            <div class='contact-box'>
                <p><strong>$questions</strong></p>
                <p>📞 +49 7031 41073-11</p>
                <p>📧 info@area710.de</p>
                <p>🕒 Mo-Fr 10:00-18:00 Uhr</p>
            </div>
        </div>
        
        <div class='footer'>
            <p>Gottlieb-Binder-Straße 2 | D-71088 Holzgerlingen</p>
            <p>area710 eine Marke der seeeye Werbung & Event GmbH</p>
        </div>
    </div>
</body>
</html>
";

$headers_customer = "MIME-Version: 1.0" . "\r\n";
$headers_customer .= "Content-type:text/html;charset=UTF-8" . "\r\n";
$headers_customer .= "From: " . RECIPIENT_NAME . " <" . RECIPIENT_EMAIL . ">" . "\r\n";
$headers_customer .= "Reply-To: " . RECIPIENT_NAME . " <" . RECIPIENT_EMAIL . ">" . "\r\n";

$mail_customer_sent = mail($email, $subject_customer, $message_customer, $headers_customer);

// ========================================
// DATENBANK SPEICHERN (Optional)
// ========================================

// Hier könnte die Anfrage in eine Datenbank gespeichert werden
// Beispiel mit PDO:
/*
try {
    $pdo = new PDO('mysql:host=localhost;dbname=area710', 'username', 'password');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    $stmt = $pdo->prepare("
        INSERT INTO bookings (
            first_name, last_name, email, phone, company,
            event_type, event_date, event_time, duration, guests,
            rooms, services, message, created_at
        ) VALUES (
            :first_name, :last_name, :email, :phone, :company,
            :event_type, :event_date, :event_time, :duration, :guests,
            :rooms, :services, :message, NOW()
        )
    ");
    
    $stmt->execute([
        ':first_name' => $firstName,
        ':last_name' => $lastName,
        ':email' => $email,
        ':phone' => $phone,
        ':company' => $company,
        ':event_type' => $eventType,
        ':event_date' => $eventDate,
        ':event_time' => $eventTime,
        ':duration' => $duration,
        ':guests' => $guests,
        ':rooms' => $roomsText,
        ':services' => $servicesText,
        ':message' => $message
    ]);
    
} catch(PDOException $e) {
    error_log("Database error: " . $e->getMessage());
}
*/

// ========================================
// ANTWORT SENDEN
// ========================================

if ($mail_owner_sent && $mail_customer_sent) {
    http_response_code(200);
    echo json_encode([
        'success' => true,
        'message' => 'Buchungsanfrage erfolgreich versendet'
    ]);
} else {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'message' => 'Fehler beim Versenden der E-Mails'
    ]);
}

// Log für Debugging (optional)
error_log("Booking request from: $email | Event: $eventDate | Rooms: $roomsText");

?>
