```markdown
# Prerequisites
- Python 3.10+
- Node.js & npm
- Groq API Key

# Installation

## 1. Repository Setup
```bash
git clone https://github.com/andreslpxz/medical-ai-dashboard-demo.git
cd medical-ai-dashboard-demo
```

## 2. Backend Configuration
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
python -m backend.main
```

## 3. Frontend Configuration
Open a new terminal session:
```bash
cd frontend
npm install
npm run dev -- --host
```

# Access
Once both services are running, access the dashboard at:
```
http://localhost:5173
```
	
