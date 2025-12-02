# NFC Container Lending System for Nanoha

A prototype O2O (Online-to-Offline) lending system using **LINE LIFF** and **FastAPI**. Users can borrow reusable containers by scanning a QR code, which triggers a transaction recorded in the backend database.

## Tech Stack

* **Frontend**: HTML5, JavaScript (Vanilla), LINE LIFF SDK
* **Backend**: Python, FastAPI
* **Database**: SQLite (Local) / SQLAlchemy
* **Tools**: Ngrok (for intranet penetration)

## Project Structure

```text
.
├── backend/
│   ├── main.py          # FastAPI application & Database logic
│   └── gen_qr.py        # Script to generate test QR codes
├── frontend/
│   └── index.html       # LIFF User Interface
├── requirements.txt     # Python dependencies
└── README.md
```

# Setup & Installation
1. Clone the repository

```Bash
git clone [https://github.com/YOUR_USERNAME/nfc-lending-system.git](https://github.com/YOUR_USERNAME/nfc-lending-system.git)
cd nfc-lending-system
```

2. Set up Virtual Environment


```Bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies

```Bash
pip install -r requirements.txt
```

4. Run the Server


```Bash
uvicorn main:app --reload
```

5. Expose Localhost (Using Ngrok)

In a separate terminal:


```Bash
ngrok http 8000
```

# Configuration
Copy the HTTPS URL from Ngrok (e.g., https://xxxx.ngrok-free.app).

Go to LINE Developers Console -> LIFF tab.

Update the Endpoint URL to https://xxxx.ngrok-free.app/liff.

Update MY_LIFF_ID in frontend/index.html with your actual LIFF ID.

# Usage
Generate a test QR code:

```Bash
python backend/gen_qr.py
```

Scan the QR code with LINE App.

Click "Borrow".

(Demo Mode) Click "Reset Status" to return the item.

# License
MIT License

Designed & Made by Kouzen Jo. 2025.