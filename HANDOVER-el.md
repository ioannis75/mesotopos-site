# Santorini Mesotopos Suites: νέο site & ανακατευθύνσεις

Οδηγίες για τον τεχνικό. Νέο στατικό site (χωρίς WordPress/PHP/βάση) για το **santorinimesotopossuites.com**, σε 5 γλώσσες (EN `/`, EL `/el/`, FR `/fr/`, DE `/de/`, IT `/it/`).

## 0. Πριν από οτιδήποτε
- Κρατήστε **πλήρες backup** του παλιού WordPress (αρχεία + βάση) από το cPanel.
- **Το email info@mesotopos.gr πρέπει να συνεχίσει να δουλεύει.** Μην αλλάξετε/σβήσετε εγγραφές **MX, SPF (TXT), DKIM, DMARC, autodiscover, mail.** του mesotopos.gr. Αλλάζουν μόνο οι εγγραφές web (`@` και `www`).
- Αν μεταφέρετε το mesotopos.gr στο Cloudflare, ελέγξτε ότι οι MX/TXT αντιγράφηκαν **πριν** αλλάξετε nameservers και στείλτε ένα δοκιμαστικό email μετά.

## 1. Ανέβασμα του site
Ανεβάστε **όλο το περιεχόμενο** του φακέλου (μαζί με τα κρυφά `.htaccess` και `_redirects`) στη ρίζα του santorinimesotopossuites.com:
- **Cloudflare Pages** (προτείνεται, δωρεάν): Workers & Pages → Create → Pages → Upload assets → ανεβάστε τον φάκελο → Custom domains: `santorinimesotopossuites.com` και `www`. Το `_redirects` εφαρμόζεται αυτόματα.
- **cPanel**: File Manager → `public_html` του domain → αφαιρέστε το WordPress (μετά το backup) → ανεβάστε τα αρχεία. Το `.htaccess` κάνει τις ανακατευθύνσεις και το https.

Τα παλιά URL του WordPress (π.χ. `/blog/rooms/junior-suite/`) ανακατευθύνονται με 301 στις αντίστοιχες ενότητες.

## 2. Ανακατευθύνσεις 301 προς https://santorinimesotopossuites.com/
| Domain | Πού ρυθμίζεται | Τι γίνεται |
|---|---|---|
| **santorinihotelmesotopos.com** | GoDaddy (DNS στο GoDaddy) | Domain → DNS → **Forwarding** → `https://santorinimesotopossuites.com`, **Permanent (301)**, Forward only. Ή: nameservers στο Cloudflare + Redirect Rule. |
| **santorinimesotopos.com** | Namecheap / Cloudflare (`buck`/`virginia`, άλλος λογαριασμός) | Βρείτε ποιος έχει αυτόν τον λογαριασμό Cloudflare, ή αλλάξτε nameservers από το Namecheap στους δικούς σας. Μετά: DNS `A @ 192.0.2.1` και `A www 192.0.2.1` **proxied (πορτοκαλί σύννεφο)** + Rules → **Redirect Rule**: hostname ∈ {santorinimesotopos.com, www.santorinimesotopos.com} → Static `https://santorinimesotopossuites.com/` 301. **Κρατήστε τις MX** αν υπάρχει email σε αυτό το domain. |
| **mesotopos.gr** (μόνο web) | Εκεί που φιλοξενείται σήμερα το web του | Σήμερα στέλνει στο `santorinimesotopos.com/wp/` (404). Αλλάξτε τον προορισμό σε `https://santorinimesotopossuites.com/` (cPanel → Domains → Redirects, 301), ή Cloudflare Redirect Rule όπως πάνω. **Μην πειράξετε MX/email.** |

## 3. Να επιβεβαιώσει ο ιδιοκτήτης
- Ο σύνδεσμος Booking.com: `https://www.booking.com/hotel/gr/mesotopos.html` (ρυθμίζεται στο `build/build.py` → `BOOKING_URL`, ή αναζήτηση/αντικατάσταση στα 5 `index.html`).
- Αν θέλει να μείνει και η online κράτηση `santorinimesotopos.reserve-online.net` ως δεύτερο κουμπί.
- Αν το banner ΕΣΠΑ πρέπει να συνεχίσει να εμφανίζεται (έχει μπει στο footer, ανοίγει την πινακίδα PDF).
- Περίοδο λειτουργίας (αν θέλουν να αναφέρεται).

## 4. Έλεγχοι μετά
- https://santorinimesotopossuites.com/ και `/el/`, `/fr/`, `/de/`, `/it/` ανοίγουν, με πράσινο λουκέτο.
- Τα 3 άλλα domains κάνουν 301 στο νέο site.
- Δοκιμαστικό email **προς και από** info@mesotopos.gr.
- Google Search Console: υποβολή `https://santorinimesotopossuites.com/sitemap.xml`.
