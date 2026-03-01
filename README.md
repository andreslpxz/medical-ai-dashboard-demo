# Radimal Insights Demo

HealthTech MVP for DICOM image analysis using FastAPI and React.

## Prerequisites

* Python 3.10+
* Node.js 18+
* npm
* Groq API Key

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/andreslpxz/medical-ai-dashboard-demo.git
cd medical-ai-dashboard-demo
```

---

## Backend Setup

### 2. Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file inside the root:

```
GROQ_API_KEY=your_api_key_here
```

### 4. Run the Backend Server

Return to the project root:

```bash
cd ..
```

Start the server:

```bash
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

---

## Frontend Setup

### 5. Install Dependencies and Start Development Server

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at:

```
http://localhost:5173
```

---

## Project Structure

```
medical-ai-dashboard-demo/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── utils/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
```

---

## Notes

* Ensure the backend is running before using the frontend.
* A valid Groq API key is required for AI analysis to function.
