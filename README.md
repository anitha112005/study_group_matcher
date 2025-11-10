# Study Group Matcher — Demo

**Project**: Effective Collaboration & Study Group Formation  
**Stack**: Flask (Python), SQLite (SQLAlchemy), simple frontend (HTML/JS/CSS).  
**CrewAI**: included as a stub wrapper (`crewai_agent.py`) with instructions for integrating CrewAI agentic capabilities.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Initialize database & load sample data:
```bash
python sample_data.py
```

3. Run the app:
```bash
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

## Notes on CrewAI integration

`crewai_agent.py` is a scaffold showing how you might call CrewAI or another agent orchestration framework. Replace placeholders with your CrewAI credentials and follow CrewAI docs.

