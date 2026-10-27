import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.question_bank import get_bank_questions

def test_combo(role, focus, difficulty, count=5):
    questions = get_bank_questions(role, focus, difficulty, count)
    print(f"\n==========================================")
    print(f"Role: {role} | Focus: {focus} | Difficulty: {difficulty} | Count: {count}")
    print(f"==========================================")
    assert len(questions) == count, f"Expected {count} questions, got {len(questions)}"
    seen = set()
    for idx, q in enumerate(questions, 1):
        assert q["question"] not in seen, f"Duplicate found: {q['question']}"
        seen.add(q["question"])
        print(f"{idx}. [{q.get('difficulty')}] {q.get('topic')}: {q.get('question')}")

# Test the 3 required combinations from user prompt:
test_combo("Python Developer", "Technical Interview", "Medium", 5)
test_combo("UI/UX Designer", "Problem Solving Interview", "Easy", 5)
test_combo("HR Interview", "Behavioral Interview", "Medium", 5)

# Test high counts (10, 15, 20)
test_combo("UI/UX Designer", "Problem Solving Interview", "Easy", 10)
test_combo("Machine Learning Engineer", "Technical Interview", "Hard", 5)
test_combo("Data Analyst", "Scenario Based Interview", "Medium", 5)
test_combo("Full Stack Developer", "Technical Interview", "Medium", 5)
