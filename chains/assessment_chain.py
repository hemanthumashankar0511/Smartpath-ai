from prompts.assessment_questions import get_questions, DOMAINS
from data import db
from typing import List, Dict, Any
import json

SKILL_LEVELS = [
    (0.0, 0.4, "Beginner"),
    (0.4, 0.8, "Intermediate"),
    (0.8, 1.1, "Advanced")
]

def score_answers(questions: list, user_answers: list) -> dict:
    """
    Scores the user's answers for the provided questions.
    Returns: dict with score, skill_level, correct_count, total
    """
    correct = 0
    for i, q in enumerate(questions):
        if i < len(user_answers) and user_answers[i].strip().lower() == q['answer'].strip().lower():
            correct += 1
    total = len(questions)
    score = correct / total if total else 0
    # Determine skill level
    for low, high, level in SKILL_LEVELS:
        if low <= score < high:
            skill_level = level
            break
    else:
        skill_level = "Unknown"
    return {
        "score": score,
        "skill_level": skill_level,
        "correct_count": correct,
        "total": total
    }

def analyze_learning_style(style_answers: List[str]) -> Dict[str, Any]:
    """
    Simple analysis of learning style answers (returns as-is for now).
    """
    return {f"q{i+1}": ans for i, ans in enumerate(style_answers)}

def run_assessment(user_id: int, domain: str, user_answers: list, questions: list, style_answers: list = None) -> dict:
    """
    Runs the assessment, scores answers, and stores results.
    Returns a summary dict.
    """
    # Score domain answers using the provided question order
    correct = 0
    question_results = []
    for i, q in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else None
        correct_answer = q['answer']
        is_correct = (user_answer is not None and user_answer.strip().lower() == correct_answer.strip().lower())
        if is_correct:
            correct += 1
        question_results.append({
            'question': q['question'],
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })
    total = len(questions)
    score = correct / total if total else 0
    # Determine skill level
    for low, high, level in SKILL_LEVELS:
        if low <= score < high:
            skill_level = level
            break
    else:
        skill_level = "Unknown"
    # Store in DB
    responses = {
        "answers": user_answers
    }
    db.add_assessment(
        user_id=user_id,
        skill_level=skill_level,
        domain=domain,
        responses=json.dumps(responses)
    )
    # Return summary
    return {
        "domain": domain,
        "score": score,
        "skill_level": skill_level,
        "correct_count": correct,
        "total": total,
        "questions": question_results
    }

if __name__ == "__main__":
    # Example usage
    user_id = 1
    domain = "python"
    questions = get_questions(domain)
    print("Sample questions:")
    for i, q in enumerate(questions[:10]):
        print(f"Q{i+1}: {q['question']} Choices: {q['choices']}")
    # Simulate user answers (all correct)
    user_answers = [q['answer'] for q in DOMAINS[domain][:10]]
    style_answers = []
    summary = run_assessment(user_id, domain, user_answers, questions, style_answers)
    print("Assessment summary:", summary) 