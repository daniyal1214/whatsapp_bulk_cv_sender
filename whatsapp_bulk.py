import time
import pandas as pd
import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === SETTINGS ===
excel_file = "contacts.xlsx"          # Your Excel file with phone numbers
cv_file = "Daniyal's_CV.pdf"            # Your CV file path
message = """Hello,

This is Daniyal Nadeem, a Software Engineer with over 2.5 years of experience in Flutter mobile application development. I have worked on multiple cross-platform projects involving UI/UX design, API integration, Firebase, Google Maps Integration, and notifications.

I am currently seeking new opportunities and would be glad to contribute my skills to your team. I am available to join immediately.

I’ve attached my CV for your review. Please let me know if there are any opportunities available that match my profile.

Best regards,
Daniyal Nadeem
"""

# === LOAD CONTACTS ===
df = pd.read_excel(excel_file)
numbers = df["PhoneNumber"].astype(str).tolist()

# === SETUP SELENIUM ===
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=/Users/macbookair/Library/Application Support/Google/Chrome/whatsapp-profile")  
options.add_argument("--profile-directory=Default")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")
print("Scan the QR code if required...")
time.sleep(20)  # wait for login

# === SEND MESSAGES ===
for idx, number in enumerate(numbers, start=1):
    try:
        encoded_message = urllib.parse.quote(message)
        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_message}"
        driver.get(url)

        # Wait until message box loads
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        time.sleep(2)

        # Press Enter to send message
        webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()
        time.sleep(3)

        # Attach CV
        try:
            # Click attachment (plus-rounded icon)
            attach_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus-rounded']"))
            )
            attach_btn.click()
            time.sleep(1)

            # Directly send the file to the hidden input without opening file picker
            file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
            file_path = os.path.abspath(cv_file)
            print("📂 Uploading file:", file_path)
            file_input.send_keys(file_path)
            time.sleep(3)

            # Click send button (wds-ic-send-filled)
            send_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='wds-ic-send-filled']"))
            )
            send_btn.click()
            time.sleep(5)

            print(f"✅ CV sent to {number}")

        except Exception as e:
            print(f"⚠️ Failed to send CV to {number}: {e}")


        print(f"[{idx}/{len(numbers)}] Sent to {number}")

    except Exception as e:
        print(f"Failed for {number}: {e}")

driver.quit()
