from data import db
from chains import assessment_chain, curriculum_chain, progress_chain
from prompts.assessment_questions import get_questions, DOMAINS, LEARNING_STYLE_QUESTIONS
import json
import time

def test_db_crud():
    print("Testing DB CRUD...")
    email = f"testuser_{int(time.time())}@example.com"
    # Clean up if user exists (shouldn't, but for safety)
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    user_id = db.add_user("Test User", email)
    user = db.get_user_by_email(email)
    assert user is not None and user[1] == "Test User"
    print("DB CRUD: PASS")
    return user_id

def test_assessment(user_id):
    print("Testing Assessment...")
    domain = "python"
    questions = get_questions(domain)
    user_answers = [q['answer'] for q in DOMAINS[domain][:10]]
    result = assessment_chain.run_assessment(user_id, domain, user_answers, questions)
    assert result['skill_level'] in ['Advanced', 'Intermediate', 'Beginner']
    print("Assessment: PASS")
    return result

def test_curriculum(user_id, assessment_result):
    print("Testing Curriculum Planner...")
    path = curriculum_chain.plan_learning_path(
        user_id=user_id,
        domain=assessment_result['domain'],
        skill_level=assessment_result['skill_level'],
        learning_style=assessment_result['learning_style'],
        study_time='<2 hours'
    )
    assert 'milestones' in path and len(path['milestones']) > 0
    print("Curriculum Planner: PASS")
    return path

def test_progress(user_id, path):
    print("Testing Progress Tracking...")
    milestones = [m['title'] for m in path['milestones']]
    completed = milestones[:2]
    progress_chain.record_progress(user_id, completed)
    progress = progress_chain.get_progress(user_id)
    assert set(progress['completed_items']) == set(completed)
    print("Progress Tracking: PASS")

def run_all_tests():
    print("--- Running All Tests ---")
    user_id = test_db_crud()
    assessment_result = test_assessment(user_id)
    path = test_curriculum(user_id, assessment_result)
    test_progress(user_id, path)
    print("All tests passed!")

if __name__ == "__main__":
    run_all_tests() 