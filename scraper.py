import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

def fetch_case_details(case_type, case_number, filing_year, captcha_token=None):
    """
    Scrapes Delhi High Court case data using Playwright (headless browser).
    CAPTCHA token must be manually obtained from the user.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Visit the Delhi High Court case status page
            url = "https://delhihighcourt.nic.in/casestatus"
            page.goto(url, timeout=20000)
            page.wait_for_load_state("load")

            # Fill the case search form
            page.select_option("#ddlCaseType", case_type)
            page.fill("#txtCaseNo", case_number)
            page.fill("#txtCaseYear", filing_year)

            # CAPTCHA token required
            if not captcha_token:
                raise ValueError("CAPTCHA token is required for Delhi High Court.")
            page.fill("#txtCaptcha", captcha_token)

            # Click the Search button
            page.click("#btnSearch")
            page.wait_for_timeout(5000)

            # Get page content and parse it
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            # Extracting details
            parties = soup.select_one("#lblParties")
            filing_date = soup.select_one("#lblFilingDate")
            next_hearing = soup.select_one("#lblNextDate")
            pdf_link = soup.find("a", string="Click here for judgment")

            result = {
                "parties": parties.text.strip() if parties else "N/A",
                "filing_date": filing_date.text.strip() if filing_date else "N/A",
                "next_hearing": next_hearing.text.strip() if next_hearing else "N/A",
                "pdf_url": pdf_link["href"] if pdf_link else None
            }

            return result

        except PlaywrightTimeout:
            raise RuntimeError("Page took too long to load or form failed to submit.")
        except Exception as e:
            raise RuntimeError(f"Error scraping court data: {e}")
        finally:
            browser.close()
