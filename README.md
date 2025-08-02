# 🏛️ Court-Data Fetcher & Dashboard

A Flask-based web app that allows users to fetch Indian court case details by entering case type, number, and year. The results are parsed and displayed beautifully, with options to download case details as PDF and view search history.

---

## 🚀 Features

- 📥 Fetch live case details (e.g. from Delhi High Court or District Courts)
- 📄 Download result as PDF
- 🕑 Highlights next hearing status (Upcoming / Expired / None)
- 🕰️ View past searches (query history)
- 🔐 CSRF & input sanitization for basic security

---

## 🛠️ Tech Stack

- **Backend**: Flask, SQLite, dotenv
- **Frontend**: HTML, CSS (custom), Jinja2
- **PDF Generation**: `xhtml2pdf`
- **Security**: CSRF tokens, HTML escaping, secret key via `.env`

---
