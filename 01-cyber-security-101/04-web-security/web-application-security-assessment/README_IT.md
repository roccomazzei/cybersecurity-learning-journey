<p align="right"><a href="README.md">🇬🇧 English</a> · <strong>🇮🇹 Italiano</strong></p>

# Lab 03 — Web Application Security Assessment

**Percorso:** TryHackMe Cyber Security 101 (Web Security + Offensive Security Tooling + OWASP Top 10)
**Sezione:** Assessment pratico combinato
**Ambiente:** VM Kali Linux, target applicazione Flask su `127.0.0.1`
**Strumenti:** Burp Suite (Proxy, Repeater), Gobuster, SQLMap, Hydra, curl

## Obiettivo

Questo lab unisce tre sezioni separate di Cyber Security 101 — **Web Security**, **Offensive Security Tooling** e **OWASP Top 10** — in un unico assessment di sicurezza web realistico, invece di tre mini-lab scollegati tra loro.

Il flusso segue un assessment standard: baseline → intercettazione proxy → discovery → verifica manuale → conferma automatica controllata → classificazione del rischio → remediation.

Tutti i test sono stati eseguiti esclusivamente contro un'applicazione target creata per questo lab, in esecuzione su `127.0.0.1`. Nessun sistema di terze parti è stato testato.

## Applicazione target

È stata costruita una piccola applicazione Flask ([`target-app/app.py`](target-app/app.py)) con due debolezze intenzionali, per poter esercitare l'intero workflow di assessment:

- `/admin` — una route di amministrazione raggiungibile senza alcun controllo di autenticazione o sessione.
- `/search?q=` — un endpoint di ricerca utenti che costruisce la query SQL concatenando direttamente il parametro `q`, rendendolo vulnerabile a SQL injection.

Una terza debolezza, non legata al codice (una password account prevedibile senza protezione anti-bruteforce), è stata inclusa nei dati utente seminati per esercitare il test di autenticazione.

```bash
mkdir -p ~/lab03-web && cd ~/lab03-web
python3 -m venv venv && source venv/bin/activate
pip install flask
python app.py   # in ascolto su http://127.0.0.1:5000
```

## Metodologia

| Fase | Attività |
|---|---|
| 1 | Baseline HTTP — mappare pagine, metodi, parametri |
| 2 | Burp Proxy / Repeater — intercettare e modificare richieste |
| 3 | Discovery — enumerazione directory con Gobuster |
| 4 | Access control — verifica aree non autenticate |
| 5 | SQL injection — verifica manuale |
| 6 | SQLMap — conferma controllata |
| 7 | Test di autenticazione — Hydra |
| 8 | Mappatura OWASP e remediation |

## Fase 1 — Baseline HTTP

Tutti e cinque gli endpoint individuati (`/`, `/login`, `/search`, `/robots.txt`, `/admin`) hanno risposto `200 OK`. In particolare, `/admin` ha restituito il contenuto completo senza alcuna richiesta di autenticazione, e lo stesso `robots.txt` rivela il path tramite la voce `Disallow: /admin` — un promemoria che `robots.txt` è una convenzione per i crawler, non un meccanismo di controllo accessi.

Evidenza: [`evidence/01-baseline-responses.txt`](evidence/01-baseline-responses.txt) · [Screenshot](screenshots/01-lab-environment.webp)

## Fase 2 — Burp Proxy & Repeater

Il browser è stato configurato per passare dal Burp Proxy. È stata intercettata una richiesta `GET /search?q=admin`, poi inviata a Repeater, dove il parametro `q` è stato modificato in `alice`; la risposta è cambiata di conseguenza, confermando che il parametro guida direttamente la logica di ricerca. È stata inoltre analizzata la richiesta `POST /login` per identificare i campi `username` e `password` del form.

| Domanda | Risposta |
|---|---|
| Quale parametro controlla la ricerca? | `q` (query string su `/search`) |
| Quali campi vengono inviati dal form di login? | `username`, `password` (POST a `/login`) |
| La risposta cambia modificando il parametro? | Sì — `q=alice` restituisce `alice - alice@lab.local` invece del risultato per admin |

Evidenza: [Screenshot intercettazione](screenshots/03-burp-proxy-intercept.webp) · [Screenshot Repeater](screenshots/04-burp-repeater-response.webp)

## Fase 3 — Discovery

```bash
curl http://lab03.local:5000/robots.txt
gobuster dir -u http://lab03.local:5000 -w /usr/share/wordlists/dirb/common.txt
```

Gobuster ha enumerato l'intera superficie dell'applicazione — `admin`, `login`, `robots.txt`, `search` — tutti con risposta `200 OK`.

Evidenza: [`evidence/03-gobuster-output.txt`](evidence/03-gobuster-output.txt) · [Screenshot](screenshots/05-gobuster-enumeration.webp)

## Fase 4 — Access Control

`GET /admin` è stata richiesta direttamente, senza alcun login o sessione precedente, restituendo il pannello di amministrazione completo (`200 OK`).

**Finding:** controllo di accesso assente su `/admin` — la route non esegue alcuna verifica di autenticazione o autorizzazione prima di servire il contenuto riservato.

Evidenza: [Screenshot](screenshots/02-manual-recon-robots-admin.webp)

## Fase 5 — SQL Injection (manuale)

| Test | Valore di `q` | Osservazione |
|---|---|---|
| Baseline | `admin` | Singolo risultato atteso |
| Quote test | `'` | Errore SQL grezzo restituito al client |
| Boolean test | `' OR '1'='1` | Tutti e tre gli utenti restituiti (clausola WHERE bypassata) |
| Comment test | `admin' --` | Contenuto finale della query neutralizzato come atteso |

Il quote test ha rotto la sintassi della query, mentre il boolean test ha restituito ogni riga della tabella `users`, confermando la concatenazione diretta e non sanificata nella query SQL.

Evidenza: [`evidence/02-sql-injection-manual.txt`](evidence/02-sql-injection-manual.txt) · [Screenshot](screenshots/06-manual-sql-injection.webp)

## Fase 6 — SQLMap (conferma controllata)

```bash
sqlmap -u "http://lab03.local:5000/search?q=admin" -p q --batch --level=1 --risk=1
```

SQLMap ha confermato il parametro `q` come iniettabile (tecnica UNION query) e ha identificato il DBMS come **SQLite**. I test sono stati fermati a questo punto — nessun `--dump` è stato eseguito, coerentemente con l'obiettivo di conferma a basso impatto del lab.

Evidenza: [`evidence/04-sqlmap-output.txt`](evidence/04-sqlmap-output.txt) · [Screenshot](screenshots/07-sqlmap-confirmation.webp)

## Fase 7 — Test di autenticazione (Hydra)

Una credenziale nota è stata verificata manualmente (`admin` / `password123`), poi Hydra è stata lanciata contro una wordlist locale di 3 voci:

```bash
printf "wrongpass\npassword123\nletmein\n" > lab-passwords.txt
hydra -l admin -P lab-passwords.txt lab03.local -s 5000 \
  http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials"
```

Hydra ha recuperato la password valida in un'unica esecuzione, senza alcun ritardo, lockout o rate limiting da parte dell'applicazione. Il finding è la credenziale debole e prevedibile e l'assenza di protezione anti-bruteforce — non il fatto che uno strumento automatico "funzioni".

Evidenza: [`evidence/05-hydra-output.txt`](evidence/05-hydra-output.txt) · [Screenshot](screenshots/08-hydra-authentication-testing.webp)

## Mappatura OWASP Top 10 (2025)

| Finding | OWASP Top 10 (2025) | Remediation |
|---|---|---|
| `/admin` raggiungibile senza autenticazione | **A01 — Broken Access Control** | Richiedere autenticazione e autorizzazione server-side; deny by default |
| SQL injection via `q` su `/search` | **A05 — Injection** | Query parametrizzate / prepared statements; validazione input |
| Password debole, nessuna protezione anti-bruteforce | **A07 — Authentication Failures** | Password policy, rate limiting, lockout controllato, MFA dove opportuno |
| Errore SQL grezzo restituito al client | **A02 — Security Misconfiguration** | Messaggi di errore generici lato client; dettagli solo nei log server |

## Concetti chiave

- Un flusso di assessment realistico — baseline, intercettazione, discovery, verifica manuale, poi conferma automatica — produce evidenze molto più solide rispetto al passare subito agli strumenti automatici.
- `robots.txt` non è un meccanismo di controllo accessi; può anzi rivelare attivamente i path da provare per primi a un attaccante.
- Le query SQL costruite per concatenazione di stringhe si rompono con un singolo apice e vengono bypassate completamente con il classico payload `OR '1'='1'`.
- SQLMap e Hydra sono strumenti di conferma: l'obiettivo era validare finding già dimostrati manualmente, con le impostazioni di risk/level più basse e senza esfiltrazione di dati.
- Restituire errori database grezzi al client è di per sé un finding (di severità minore), perché rivela dettagli implementativi utili a un attaccante.

## Riepilogo remediation

- Aggiungere autenticazione e controlli di autorizzazione server-side a `/admin`.
- Sostituire la query SQL costruita per concatenazione di stringhe in `/search` con una query parametrizzata.
- Applicare una password policy e aggiungere rate limiting / account lockout su `/login`.
- Sostituire il testo grezzo delle eccezioni nelle risposte HTTP con un messaggio di errore generico, loggando i dettagli completi solo lato server.

## Etica e scope

Tutti i test di questo lab sono stati eseguiti esclusivamente contro l'applicazione target descritta sopra, in esecuzione su `127.0.0.1` sotto il mio controllo diretto. Nessun sistema di terze parti è stato scansionato, sfruttato o testato in altro modo. SQLMap e Hydra sono stati eseguiti con le impostazioni di risk/level più basse possibili e fermati non appena ogni finding è stato confermato, senza dump del database e senza alcun uso della credenziale recuperata oltre alla verifica.
