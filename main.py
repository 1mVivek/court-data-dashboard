from flask import Flask, render_template, request
from scraper import fetch_case_details
from storage import log_query
import os

app = Flask(__name__)  # ⬅️ FIXED: Use __name__, not name

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        case_type = request.form["case_type"]
        case_number = request.form["case_number"]
        filing_year = request.form["filing_year"]
        captcha_token = request.form.get("captcha_token")  # Optional field

        try:
            result = fetch_case_details(case_type, case_number, filing_year, captcha_token)
            log_query(case_type, case_number, filing_year, result)
            return render_template("result.html", result=result)
        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":  # ⬅️ FIXED: __name__ and "__main__"
    app.run(debug=True)
