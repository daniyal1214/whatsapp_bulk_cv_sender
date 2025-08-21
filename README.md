# 📲 WhatsApp Bulk Sender with CV Attachment

This Python script automates sending personalized **WhatsApp messages** along with a **PDF attachment (CV)** to multiple contacts.  
It uses **Selenium WebDriver** to interact with [WhatsApp Web](https://web.whatsapp.com) and works seamlessly with your existing Chrome profile.

---

## ✨ Features
- Send a **custom message** to multiple contacts.
- Automatically **attach a CV (PDF file)** with each message.
- Uses your **saved WhatsApp login session** (no need to scan QR every time).
- Reads contacts directly from an **Excel file**.

---

# 2️⃣ Setup Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

---

# 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

(If you don’t have a requirements.txt, install directly:)

```bash
pip install selenium pandas openpyxl webdriver-manager
```

---

# 📑 Excel File Format

Your EXCEL.xlsx file must have a column named **PhoneNumber(Required)** with phone numbers in international format (without +).

Example:

PhoneNumber
923001234567
923451234567
923331234567

---

# ▶️ Usage

Place your CV file in the same folder as the script and update the filename in whatsapp_bulk.py:


CV_FILE = "CV.pdf"


Run the script:

```bash
python whatsapp_bulk.py
```

On the first run, scan the WhatsApp Web QR Code when prompted. Your session will be saved for future runs.

---

# ⚠️ Important Notes

Ensure you have ***Google Chrome*** installed.

WhatsApp may temporarily block you if you send too many messages in a short time. Use responsibly.

This script is intended for ***personal/job-hunting purposes only***, not for spam.

---