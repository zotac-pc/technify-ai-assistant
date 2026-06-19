# TAIA Setup & Deployment Guide

Welcome to the Technify Academic AI Assistant (TAIA) project! This guide contains everything your team members need to know to pull the code, install dependencies, and run the project in either **Development Mode** or **Production Mode**.

## 1. Prerequisites Installation

Before pulling the code, ensure your system has the following installed:

### Git & Python
- **Git:** Download and install from [git-scm.com](https://git-scm.com/)
- **Python 3.10+:** Download and install from [python.org](https://www.python.org/)

### Docker Desktop (For Production Mode)
- **Windows/Mac:** Download [Docker Desktop](https://www.docker.com/products/docker-desktop/) and run the installer.
- **Note:** Make sure WSL2 is enabled if you are on Windows.

### Redis (Optional for Dev, Required for Production)
- *Note: TAIA has an automatic in-memory fallback if Redis is not installed, so your app will never crash without it.*
- **Windows:** The easiest way to run Redis on Windows is via Docker (covered in Production mode). Alternatively, you can install Redis via WSL (Windows Subsystem for Linux) using `sudo apt install redis-server`.

---

## 2. Getting Started (Git Pull)

Open your terminal and run the following commands to get the code and install the Python dependencies:

```bash
# 1. Clone the repository
git clone https://github.com/your-org/technify-ai-assistant.git
cd technify-ai-assistant

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Generate Mock Data & Vector Store
# Since data files are ignored by git, you must generate them locally:
python scripts/generate_data.py
python scripts/ingest_documents.py
```

Create a `.env` file in the root directory with the following variables:
```env
LLM_API_KEY=your_openrouter_or_groq_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/free
APP_HOST=0.0.0.0
APP_PORT=8000
ERP_API_BASE_URL=http://localhost:8001/api/v1
CORS_ORIGINS=http://localhost:3000,http://localhost:5000,http://localhost:8080
```

---

## 3. Running in Development Mode (Local Testing)

In development mode, we run the services directly on our machine without Docker. This is great for debugging and making quick code changes.

You will need **three separate terminal windows**. Make sure your virtual environment (`venv`) is activated in all three!

**Terminal 1 (Mock ERP API):**
```bash
uvicorn mock_erp.main:app --port 8001
```

**Terminal 2 (FastAPI AI Brain):**
```bash
python -m app.main
```

**Terminal 3 (Frontend UI):**
```bash
python ui_app/app.py
```

Once all three are running, open your browser and go to: `http://127.0.0.1:5000`

---

## 4. Running in Production Mode (Docker)

For the final production deployment, we use `docker-compose` to spin up everything simultaneously (including a dedicated Redis container).

1. Ensure **Docker Desktop** is open and running in the background.
2. Open a single terminal in the project directory.
3. Run the deployment command:
   ```bash
   docker-compose up --build -d
   ```
4. The system will pull the Redis image, build the FastAPI Gateway with Gunicorn, and start the Mock ERP.
5. You can view the live logs at any time by running:
   ```bash
   docker-compose logs -f
   ```
6. To shut down the production environment:
   ```bash
   docker-compose down
   ```

---

## 5. Using the UI & Authentication

When you open the UI, you will see two authentication options:

### Option A: The "Dev Fallback" (For Testing)
During local development, you don't need a real token. Simply use the dropdown menu to select your role (`Student`, `Faculty`, or `Admin`) and enter an ID (like `STU-0001`). This bypasses the security check for easy testing.

### Option B: The Production JWT Token
In a real-world scenario, the user would log into the University's main portal (SSO). The university portal would generate a **JSON Web Token (JWT)** and pass it to TAIA. 

To test this production flow locally, you can generate a real JWT using the built-in security handler. Run this quick python script in your terminal (with the venv activated):
```bash
python -c "from app.auth.jwt_handler import create_access_token; print(create_access_token({'sub': 'STU-0001', 'role': 'Student'}))"
```
Copy the long string it prints, paste it into the **"Paste JWT Bearer Token Here..."** field in the UI, and click **Save Token**.

---

## 6. Accessing the Admin Audit Logs

Member 5 implemented a persistent SQLite database (`.audit.db`) that tracks every question asked, the latency, and the user's role.

### How to view the logs:

We have built a dedicated **Admin Dashboard** directly into the frontend!

**To authenticate and view the dashboard:**
1. Open the Chat UI (`http://127.0.0.1:5000`).
2. Use the Dev Fallback to set your role to **Admin**.
3. Click the red **🛡️ Admin Dashboard** button in the sidebar.
4. The dashboard will automatically fetch and display all queries, latencies, and intents in a professional UI!

*(If you are building external integrations, the raw JSON data is also fully accessible via `GET http://127.0.0.1:8000/api/v1/admin/audit-logs` by passing an Admin JWT or `x-user-role: Admin` header).*
