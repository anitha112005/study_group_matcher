from models import session_scope, Student
from collections import defaultdict
import math

def availability_overlap(a_list, b_list):
    # naive string overlap measure: count matching day tokens
    days_a = set([x.split()[0] for x in a_list])
    days_b = set([x.split()[0] for x in b_list])
    return len(days_a & days_b)

def match_score(target, candidate):
    # Compute a simple score based on:
    # - number of shared courses (weighted)
    # - GPA proximity (smaller difference is better)
    # - availability overlap
    shared_courses = len(set(target.courses or []) & set(candidate.courses or []))
    gpa_diff = abs((target.gpa or 0) - (candidate.gpa or 0))
    avail_overlap = availability_overlap(target.availability or [], candidate.availability or [])

    # score formula (tunable)
    score = (shared_courses * 4.0) + (max(0, 4 - gpa_diff)) + (avail_overlap * 2.0)
    return round(score, 3)

def match_for_student(db_path, student_id, top_n=5):
    with session_scope(db_path) as session:
        target = session.query(Student).filter_by(id=student_id).first()
        if target is None:
            return {"error": "student not found"}
        candidates = session.query(Student).filter(Student.id != student_id).all()
        scored = []
        for c in candidates:
            s = match_score(target, c)
            scored.append({"student": c.to_dict(), "score": s})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_n]
