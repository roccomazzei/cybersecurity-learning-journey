<p align="right"><strong>🇬🇧 English</strong> · <a href="README_IT.md">🇮🇹 Italiano</a></p>

# Lab 03 — Web Application Security Assessment

**Path:** TryHackMe Cyber Security 101 (Web Security + Offensive Security Tooling + OWASP Top 10)
**Section:** Combined practical assessment
**Environment:** Kali Linux VM, target Flask application on `127.0.0.1`
**Tools:** Burp Suite (Proxy, Repeater), Gobuster, SQLMap, Hydra, curl

## Objective

This lab combines three separate Cyber Security 101 sections — **Web Security**, **Offensive Security Tooling**, and **OWASP Top 10** — into a single, realistic web application security assessment rather than three disconnected mini-labs.

The workflow follows a standard assessment flow: baseline → proxy interception → discovery → manual verification → controlled automated confirmation → risk classification → remediation.

All testing was performed exclusively against a target application built for this lab, running on `127.0.0.1`. No third-party systems were tested.

## Target Application

A small Flask application ([`target-app/app.py`](target-app/app.py)) was built with two deliberate weaknesses so the assessment workflow could be exercised end to end:

- `/admin` — an administration route reachable with no authentication or session check.
- `/search?q=` — a user search endpoint that builds its SQL query by directly concatenating the `q` parameter, making it vulnerable to SQL injection.

A third, non-coding weakness (a predictable account password with no brute-force protection) was also included in the seeded user data to exercise authentication testing.

```bash
mkdir -p ~/lab03-web && cd ~/lab03-web
python3 -m venv venv && source venv/bin/activate
pip install flask
python app.py   # serves on http://127.0.0.1:5000
```

## Methodology

| Phase | Activity |
|---|---|
| 1 | Baseline HTTP — map pages, methods, parameters |
| 2 | Burp Proxy / Repeater — intercept and modify requests |
| 3 | Discovery — Gobuster directory enumeration |
| 4 | Access control — verify unauthenticated areas |
| 5 | SQL injection — manual verification |
| 6 | SQLMap — controlled confirmation |
| 7 | Authentication testing — Hydra |
| 8 | OWASP mapping and remediation |

## Phase 1 — Baseline HTTP

All five discovered endpoints (`/`, `/login`, `/search`, `/robots.txt`, `/admin`) responded `200 OK`. Notably, `/admin` returned its full content with no authentication prompt at all, and `robots.txt` itself discloses the path via a `Disallow: /admin` entry — a reminder that `robots.txt` is a convention for crawlers, not an access control mechanism.

Evidence: [`evidence/01-baseline-responses.txt`](evidence/01-baseline-responses.txt) · [Screenshot](screenshots/01-lab-environment.webp)

## Phase 2 — Burp Proxy & Repeater

The browser was configured to route through Burp Proxy. A `GET /search?q=admin` request was intercepted, then sent to Repeater, where the `q` parameter was changed to `alice`; the response changed accordingly, confirming the parameter directly drives the search logic. The `POST /login` request was also inspected to identify its `username` and `password` form fields.

| Question | Answer |
|---|---|
| Which parameter controls the search? | `q` (query string on `/search`) |
| Which fields does the login form submit? | `username`, `password` (POST to `/login`) |
| Does the response change when the parameter is edited? | Yes — `q=alice` returns `alice - alice@lab.local` instead of the admin result |

Evidence: [Proxy intercept screenshot](screenshots/03-burp-proxy-intercept.webp) · [Repeater screenshot](screenshots/04-burp-repeater-response.webp)

## Phase 3 — Discovery

```bash
curl http://lab03.local:5000/robots.txt
gobuster dir -u http://lab03.local:5000 -w /usr/share/wordlists/dirb/common.txt
```

Gobuster enumerated the application's full surface — `admin`, `login`, `robots.txt`, `search` — all returning `200 OK`.

Evidence: [`evidence/03-gobuster-output.txt`](evidence/03-gobuster-output.txt) · [Screenshot](screenshots/05-gobuster-enumeration.webp)

## Phase 4 — Access Control

`GET /admin` was requested directly, with no prior login or session of any kind, and returned the full administration panel content (`200 OK`).

**Finding:** Broken access control on `/admin` — the route performs no authentication or authorization check before serving restricted content.

Evidence: [Screenshot](screenshots/02-manual-recon-robots-admin.webp)

## Phase 5 — SQL Injection (Manual)

| Test | Value of `q` | Observation |
|---|---|---|
| Baseline | `admin` | Single expected row |
| Quote test | `'` | Raw SQL error returned to the client |
| Boolean test | `' OR '1'='1` | All three users returned (WHERE clause bypassed) |
| Comment test | `admin' --` | Trailing query content neutralized as expected |

The quote test broke the query syntax and the boolean test returned every row in the `users` table, confirming unsanitized string concatenation in the SQL statement.

Evidence: [`evidence/02-sql-injection-manual.txt`](evidence/02-sql-injection-manual.txt) · [Screenshot](screenshots/06-manual-sql-injection.webp)

## Phase 6 — SQLMap (Controlled Confirmation)

```bash
sqlmap -u "http://lab03.local:5000/search?q=admin" -p q --batch --level=1 --risk=1
```

SQLMap confirmed the `q` parameter as injectable (UNION query technique) and fingerprinted the back-end DBMS as **SQLite**. Testing was stopped at that point — no `--dump` was performed, consistent with the lab's minimal-impact confirmation goal.

Evidence: [`evidence/04-sqlmap-output.txt`](evidence/04-sqlmap-output.txt) · [Screenshot](screenshots/07-sqlmap-confirmation.webp)

## Phase 7 — Authentication Testing (Hydra)

A known credential was confirmed manually (`admin` / `password123`), then Hydra was run against a 3-entry local wordlist:

```bash
printf "wrongpass\npassword123\nletmein\n" > lab-passwords.txt
hydra -l admin -P lab-passwords.txt lab03.local -s 5000 \
  http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials"
```

Hydra recovered the valid password in a single run, with no delay, lockout, or rate limiting from the application. The finding is the weak, predictable credential and the absence of brute-force protection — not that an automated tool "worked."

Evidence: [`evidence/05-hydra-output.txt`](evidence/05-hydra-output.txt) · [Screenshot](screenshots/08-hydra-authentication-testing.webp)

## OWASP Top 10 (2025) Mapping

| Finding | OWASP Top 10 (2025) | Remediation |
|---|---|---|
| `/admin` reachable with no auth check | **A01 — Broken Access Control** | Require server-side authentication and authorization; deny by default |
| SQL injection via `q` on `/search` | **A05 — Injection** | Parameterized queries / prepared statements; input validation |
| Weak password, no brute-force protection | **A07 — Authentication Failures** | Password policy, rate limiting, controlled lockout, MFA where appropriate |
| Raw SQL error returned to the client | **A02 — Security Misconfiguration** | Generic client-facing error messages; details logged server-side only |

## Key Takeaways

- A realistic assessment flow — baseline, interception, discovery, manual verification, then automated confirmation — produces far stronger evidence than jumping straight to automated tools.
- `robots.txt` is not an access control mechanism; it can actively disclose the paths an attacker should try first.
- String-concatenated SQL queries are trivially broken by a single quote and fully bypassed with a classic `OR '1'='1'` payload.
- SQLMap and Hydra are confirmation tools: the goal was to validate findings already demonstrated manually, with the lowest risk/level settings and no data exfiltration.
- Returning raw database errors to the client is itself a (lower-severity) finding, since it leaks implementation details useful to an attacker.

## Remediation Summary

- Add authentication and server-side authorization checks to `/admin`.
- Replace the string-formatted SQL query in `/search` with a parameterized query.
- Enforce a password policy and add rate limiting / account lockout on `/login`.
- Replace raw exception text in HTTP responses with a generic error message, logging full details server-side only.

## Ethics and Scope

All testing in this lab was performed exclusively against the target application described above, running on `127.0.0.1` under my own control. No third-party systems were scanned, exploited, or otherwise tested. SQLMap and Hydra were run with the lowest practical risk/level settings and stopped as soon as each finding was confirmed, with no database dump and no use of the recovered credential beyond verification.
