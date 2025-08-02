import os
import json
import html
import logging
import secrets
from io import BytesIO
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, make_response
)
from werkzeug.middleware.proxy_fix import ProxyFix
from xhtml2pdf import pisa
from dotenv import load_dotenv

from scraper import fetch_case_details
from storage import log_query, get_all_queries

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(16))
app.wsgi_app = ProxyFix(app.wsgi_app)

logging.basicConfig(level=logging.INFO)

def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(16)
    return session["_csrf_token"]

app.jinja_env.globals["csrf_token"] = generate_csrf_token

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        form_token = request.form.get("_csrf_token")
        if not form_token or form_token != session.get("_csrf_token"):
            flash("Invalid CSRF token. Please refresh and try again.")
            return redirect(url_for("index"))

        case_type = html.escape(request.form.get("case_type", "").strip())
        case_number = html.escape(request.form.get("case_number", "").strip())
        filing_year = html.escape(request.form.get("filing_year", "").strip())
        captcha_token = html.escape(request.form.get("captcha_token", "").strip())

        if not all([case_type, case_number, filing_year]):
            flash("All fields are required.")
            return redirect(url_for("index"))

        try:
            result = fetch_case_details(case_type, case_number, filing_year, captcha_token)

            if not result:
                flash("No data found for the given case.")
                return redirect(url_for("index"))

            next_hearing = result.get("next_hearing")
            if next_hearing:
                try:
                    hearing_date = datetime.strptime(next_hearing, "%Y-%m-%d")
                    result["hearing_status"] = "expired" if hearing_date < datetime.today() else "upcoming"
                except ValueError:
                    result["hearing_status"] = "unknown"
            else:
                result["hearing_status"] = "none"

            log_query(case_type, case_number, filing_year, result)
            return render_template("result.html", result=result)

        except Exception as e:
            logging.exception("Error fetching case details")
            flash("Something went wrong while fetching the case. Try again later.")
            return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/history")
def history():
    try:
        queries = get_all_queries()
        return render_template("history.html", queries=queries)
    except Exception as e:
        logging.exception("Error loading history")
        flash("Could not load history.")
        return redirect(url_for("index"))

@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    form_token = request.form.get("_csrf_token")
    if not form_token or form_token != session.get("_csrf_token"):
        flash("Invalid CSRF token. Refresh and try again.")
        return redirect(url_for("index"))

    try:
        data = json.loads(request.form.get("data", "{}"))
        html_content = render_template("result.html", result=data)

        # Consider using @media print to hide buttons in CSS instead
        html_content = html_content.replace("<form", "<!--form").replace("</form>", "</form-->")

        result_pdf = BytesIO()
        pisa.CreatePDF(BytesIO(html_content.encode("utf-8")), dest=result_pdf)

        response = make_response(result_pdf.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=case_details.pdf"
        response.headers["Content-Type"] = "application/pdf"
        return response

    except Exception as e:
        logging.exception("PDF generation error")
        flash("Could not generate PDF.")
        return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)