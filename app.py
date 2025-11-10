from flask import Flask, request, jsonify, render_template
from models import init_db, SessionLocal, Student, load_sample_students
from matching import match_for_student
from crewai_agent import CrewAIAgent

app = Flask(__name__)
DB_PATH = "students.db"

# initialize DB and load sample data if needed
init_db(DB_PATH)
# load_sample_students will not overwrite existing DB by default
load_sample_students(DB_PATH, overwrite=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/students", methods=["GET"])
def list_students():
    with SessionLocal(DB_PATH) as session:
        students = session.query(Student).all()
        return jsonify([s.to_dict() for s in students])

@app.route("/api/match/<int:student_id>", methods=["GET"])
def get_matches(student_id):
    top_n = int(request.args.get("n", 5))
    matches = match_for_student(DB_PATH, student_id, top_n=top_n)
    return jsonify(matches)

@app.route("/api/match", methods=["POST"])
def match_post():
    data = request.json
    student_id = data.get("student_id")
    if student_id is None:
        return jsonify({"error": "student_id required"}), 400
    top_n = int(data.get("n", 5))
    matches = match_for_student(DB_PATH, student_id, top_n=top_n)
    return jsonify(matches)

@app.route("/api/agent/suggest", methods=["POST"])
def agent_suggest():
    payload = request.json or {}
    # Example: call the CrewAI agent with a request to synthesize study group suggestions
    agent = CrewAIAgent()
    # This function uses DB to gather context and then calls the agent (stub or real)
    result = agent.suggest_groups(DB_PATH, payload)
    return jsonify(result)

if __name__ == "__main__":
    # Bind to the port provided by the environment (Render, Heroku, etc.)
    import os
    port = int(os.environ.get("PORT", 5000))
    # Listen on all interfaces so the container/host can reach the app
    host = os.environ.get("HOST", "0.0.0.0")
    debug_flag = os.environ.get("FLASK_DEBUG", "") == "1"
    app.run(debug=debug_flag, host=host, port=port)
