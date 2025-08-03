import os
import time
import base64
import logging
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

CAPSOLVER_API_KEY = os.getenv("CAPSOLVER_API_KEY")

def solve_captcha(session, captcha_url):
    try:
        captcha_response = session.get(captcha_url)
        if captcha_response.status_code != 200:
            raise Exception("Failed to download CAPTCHA image.")

        img_base64 = base64.b64encode(captcha_response.content).decode()

        task_payload = {
            "clientKey": CAPSOLVER_API_KEY,
            "task": {
                "type": "ImageToTextTask",
                "body": img_base64
            }
        }

        response = requests.post("https://api.capsolver.com/createTask", json=task_payload)
        result = response.json()

        if result.get("errorId") != 0:
            raise Exception(f"CapSolver Error: {result.get('errorDescription')}")

        task_id = result["taskId"]
        result_payload = {
            "clientKey": CAPSOLVER_API_KEY,
            "taskId": task_id
        }

        for _ in range(20):
            poll = requests.post("https://api.capsolver.com/getTaskResult", json=result_payload).json()
            if poll.get("status") == "ready":
                return poll["solution"]["text"]
            time.sleep(1)

        raise Exception("CAPTCHA solving timed out.")
    except Exception as e:
        logging.exception("CAPTCHA solving failed")
        raise

def fetch_case_details(case_type, case_number, filing_year, _unused_token=None):
    try:
        session = requests.Session()

        # Step 1: Load the form page
        form_url = "https://delhihighcourt.nic.in/case.asp"
        form_page = session.get(form_url)
        if form_page.status_code != 200:
            raise Exception("Failed to load case search page.")

        soup = BeautifulSoup(form_page.text, "html.parser")
        captcha_img_tag = soup.find("img", {"id": "c_captcha"})
        if not captcha_img_tag or not captcha_img_tag["src"]:
            raise Exception("CAPTCHA image not found.")

        # Step 2: Solve CAPTCHA
        captcha_url = "https://delhihighcourt.nic.in/" + captcha_img_tag["src"]
        captcha_text = solve_captcha(session, captcha_url)

        # Step 3: Prepare form data
        payload = {
            "ctype": case_type,
            "cno": case_number,
            "cyear": filing_year,
            "captcha": captcha_text,
            "submit": "Submit"
        }

        headers = {
            "Referer": form_url,
            "User-Agent": "Mozilla/5.0"
        }

        # Step 4: Submit form
        response = session.post("https://delhihighcourt.nic.in/case.asp", data=payload, headers=headers)
        if response.status_code != 200:
            raise Exception("Failed to submit case form.")

        soup = BeautifulSoup(response.text, "html.parser")

        # Step 5: Parse results
        tables = soup.find_all("table")
        if not tables or len(tables) < 2:
            raise Exception("Case details not found. Check input or CAPTCHA.")

        case_data = {
            "case_type": case_type,
            "case_number": case_number,
            "filing_year": filing_year,
            "parties": tables[1].text.strip(),
            "status": "Success"
        }

        # You can add more parsing here if more structured info is available

        return case_data

    except Exception as e:
        logging.exception("Failed to fetch case details.")
        return None
