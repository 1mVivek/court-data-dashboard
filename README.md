# 🏛️ Court-Data Fetcher & Mini-Dashboard

A web-based tool to fetch Indian court case metadata and hearing updates from case numbers, built using Flask. Supports search history tracking and PDF export of case results.

## 🚀 Features

- ✅ Search case by type, number, and filing year
- 🧠 Automatically classify upcoming or expired hearings
- 🧾 Download case details as PDF
- 📜 View search history
- 🔒 Secure CSRF protection and input sanitization
- 📦 Lightweight and easy to deploy

---

## 🛠️ Tech Stack

- Python 3
- Flask
- HTML / CSS / Bootstrap
- SQLite (for logging history)
- xhtml2pdf (for PDF generation)

---

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Create and activate virtual environment

python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

4. Set up .env

Create a .env file in the root folder:

SECRET_KEY=your-very-secret-key

Generate a secret key using:

import secrets
print(secrets.token_hex(32))


---

🖥️ Running the App

python app.py

Then visit http://127.0.0.1:5000 in your browser.


---

📝 Deployment (Optional)

You can deploy this to:

Render

Railway

Heroku

Vercel (with Flask serverless wrapper)



---

📄 License

This project is licensed under the MIT License.


---

👤 Author

Vivek Kharwar

🔗 GitHub

💼 AI & ML Enthusiast | BCA Student



---

📬 Contributions

Contributions, ideas, and bug reports are welcome! Feel free to fork the repo and open a PR.
