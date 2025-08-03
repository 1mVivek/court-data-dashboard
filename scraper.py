import time
import os
import base64
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

CAPSOLVER_API_KEY = os.getenv("CAPSOLVER_API_KEY")

def solve_captcha(image_base64):
    url = "https://api.capsolver.com/createTask"
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "ImageToTextTask",
            "body": image_base64
        }
    }
    response = requests.post(url, json=payload).json()
    
    if response.get("errorId", 0) != 0:
        raise Exception(f"CapSolver error: {response.get('errorDescription')}")

    task_id = response.get("taskId")

    # Polling result
    while True:
        res = requests.post("https://api.capsolver.com/getTaskResult", json={
            "clientKey": CAPSOLVER_API_KEY,
            "taskId": task_id
        }).json()

        if res.get("status") == "ready":
            return res["solution"]["text"]

        time.sleep(2)

def fetch_case_details(case_type, case_number, filing_year):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("https://delhihighcourt.nic.in/casestatus", timeout=20000)
            page.wait_for_load_state("load")

            # Capture captcha
            captcha = page.locator("#imgCaptcha")
            captcha_screenshot = captcha.screenshot()
            image_base64 = base64.b64encode(captcha_screenshot).decode("utf-8")

            captcha_text = solve_captcha(image_base64)

            # Fill form
            page.select_option("#ddlCaseType", case_type)
            page.fill("#txtCaseNo", case_number)
            page.fill("#txtCaseYear", filing_year)
            page.fill("#txtCaptcha", captcha_text)
            page.click("#btnSearch")
            page.wait_for_timeout(5000)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            parties = soup.select_one("#lblParties")
            filing_date = soup.select_one("#lblFilingDate")
            next_hearing = soup.select_one("#lblNextDate")
            pdf_link = soup.find("a", string="Click here for judgment")

            return {
                "parties": parties.text.strip() if parties else "N/A",
                "filing_date": filing_date.text.strip() if filing_date else "N/A",
                "next_hearing": next_hearing.text.strip() if next_hearing else "N/A",
                "pdf_url": pdf_link["href"] if pdf_link else None
            }

        except PlaywrightTimeout:
            raise RuntimeError("Timeout during scraping.")
        except Exception as e:
            raise RuntimeError(f"Scraper error: {e}")
        finally:
            browser.close()
