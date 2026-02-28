# Radimal Insights Demo

HealthTech MVP for DICOM image analysis using FastAPI and React.

## Prerequisites

- Python 3.10+
- Node.js & npm
- Groq API Key

## Installation

### 1. Repository Setup

```bash
git clone https://github.com/andreslpxz/medical-ai-dashboard-demo.git
cd medical-ai-dashboard-demo
```

### 2. Backend Configuration

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:

```
GROQ_API_KEY=your_api_key_here
```

Start the server:

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Frontend Configuration

```bash
cd frontend
npm install
npm run dev
```

## Access

Access the dashboard at:

```
http://localhost:5173
```
