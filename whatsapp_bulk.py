import time
import pandas as pd
import os
import urllib.parse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# === SETTINGS ===
excel_file = "YOUR_EXCEL.xlsx"   # Replace with your Excel file with phone numbers
cv_file = "CV.pdf"               # Your CV file path
message = """This is a test message. Please find my CV attached for your reference."""  # Customize your message here


# === LOGGING FUNCTION ===
def log(msg, level="INFO"):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{level}] {msg}")


# === LOAD CONTACTS ===
try:
    df = pd.read_excel(excel_file)
    numbers = df["PhoneNumber"].astype(str).tolist()
    log(f"Loaded {len(numbers)} contacts from Excel file '{excel_file}'.")
except Exception as e:
    log(f"Failed to read contacts: {e}", "ERROR")
    exit(1)


# === SETUP SELENIUM ===
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=/Users/macbookair/Library/Application Support/Google/Chrome/whatsapp-profile")
options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
log("Opening WhatsApp Web. Please scan the QR code if required...")
time.sleep(20)  # Wait for QR scan and loading


# === SEND MESSAGES ===
for idx, number in enumerate(numbers, start=1):
    log(f"Processing contact {idx}/{len(numbers)}: {number}")

    try:
        encoded_message = urllib.parse.quote(message)
        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_message}"
        driver.get(url)

        # Retry mechanism for chat box
        success = False
        for attempt in range(3):  # 3 retries max
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
                )
                time.sleep(2)
                webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
                success = True
                break
            except Exception as e:
                log(f"Retry {attempt+1}/3: Chat box not ready yet ({e})", "WARNING")
                time.sleep(5)

        if not success:
            log(f"Skipping {number}, chat box did not load.", "ERROR")
            continue

        # Attach CV
        try:
            attach_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus-rounded']"))
            )
            attach_btn.click()
            time.sleep(1)

            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_path = os.path.abspath(cv_file)
            log(f"📂 Uploading file: {file_path}")
            file_input.send_keys(file_path)
            time.sleep(3)

            send_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='wds-ic-send-filled']"))
            )
            send_btn.click()
            time.sleep(5)

            log(f"✅ Successfully sent message + CV to {number}", "SUCCESS")

        except Exception as e:
            log(f"⚠️ Failed to send CV to {number}: {e}", "ERROR")

    except Exception as e:
        log(f"❌ Unexpected error for {number}: {e}", "ERROR")


driver.quit()
log("All tasks completed. Browser closed.", "SUCCESS")
