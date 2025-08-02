from flask import make_response
from xhtml2pdf import pisa
from io import BytesIO
import json

@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    form_token = request.form.get("_csrf_token")
    if not form_token or form_token != session.get("_csrf_token"):
        flash("Invalid CSRF token. Refresh and try again.")
        return redirect(url_for('index'))

    try:
        data = json.loads(request.form.get("data", "{}"))
        html_content = render_template("result.html", result=data)
        
        # Remove buttons from PDF
        html_content = html_content.replace('<form', '<!--form').replace('</form>', '</form-->')

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
