from langchain_community.llms import Ollama
import json
from data import db
from typing import Dict, Any

def plan_learning_path(user_id: int, assessment_result: Dict[str, Any], study_time: str) -> Dict[str, Any]:
    """
    Generate a personalized learning path using the LLM, based on assessment results and study time.
    assessment_result: dict with keys 'domain', 'skill_level', 'questions' (list of dicts with question, user_answer, correct_answer, is_correct)
    study_time: string, e.g. '<2 hours', '2-5 hours', etc.
    Returns: dict with path summary
    """
    domain = assessment_result['domain']
    skill_level = assessment_result['skill_level']
    questions = assessment_result['questions']
    # Prepare a detailed, structured prompt
    prompt = (
        f"You are an expert curriculum designer.\n"
        f"The user took an assessment in the domain '{domain}'.\n"
        f"Their skill level is: {skill_level}.\n"
        f"They can study per week: {study_time}.\n"
        f"Here are their answers (with correctness):\n"
    )
    for i, q in enumerate(questions):
        prompt += (
            f"Q{i+1}: {q['question']}\n"
            f"User answer: {q['user_answer']}\n"
            f"Correct answer: {q['correct_answer']}\n"
            f"Is correct: {q['is_correct']}\n"
        )
    prompt += (
        "\nBased on this, generate a personalized learning path as a JSON object with the following structure:\n"
        "{\n  'title': str,\n  'domain': str,\n  'milestones': [\n    { 'title': str, 'description': str }\n  ],\n  'timeline_weeks': int,\n  'skill_level': str\n}\n"
        "- Focus on weak areas (incorrect answers), but include a review of basics if needed.\n"
        "- Make the number of milestones and timeline realistic for the user's study time.\n"
        "- Each milestone should be actionable and clear.\n"
        "- Respond ONLY with the JSON object."
    )
    llm = Ollama(model="llama3.2:3b")
    response = llm(prompt)
    # Try to parse the LLM's response as JSON
    try:
        # Sometimes LLMs wrap JSON in code blocks
        if response.strip().startswith('```'):
            response = response.strip().split('```')[1]
        path = json.loads(response)
    except Exception as e:
        # Fallback: return a minimal path
        path = {
            'title': f"{domain.title()} Learning Path",
            'domain': domain,
            'milestones': [],
            'timeline_weeks': 8,
            'skill_level': skill_level
        }
    # Store in DB
    db_conn = db.get_connection()
    c = db_conn.cursor()
    c.execute(
        "INSERT INTO learning_paths (user_id, title, milestones, timeline) VALUES (?, ?, ?, ?)",
        (user_id, path['title'], json.dumps(path['milestones']), str(path['timeline_weeks']))
    )
    db_conn.commit()
    db_conn.close()
    return path

if __name__ == "__main__":
    # Example usage
    user_id = 1
    domain = 'python'
    skill_level = 'Beginner'
    questions = [
        {'question': 'What is Python?', 'user_answer': 'A programming language', 'correct_answer': 'A programming language', 'is_correct': True},
        {'question': 'What is the correct syntax for a function?', 'user_answer': 'def', 'correct_answer': 'def', 'is_correct': True},
        {'question': 'What is the correct syntax for a for loop?', 'user_answer': 'for', 'correct_answer': 'for', 'is_correct': True},
        {'question': 'What is the correct syntax for a while loop?', 'user_answer': 'while', 'correct_answer': 'while', 'is_correct': True},
        {'question': 'What is the correct syntax for a list?', 'user_answer': '[]', 'correct_answer': '[]', 'is_correct': True}
    ]
    study_time = '<2 hours'
    assessment_result = {
        'domain': domain,
        'skill_level': skill_level,
        'questions': questions
    }
    path = plan_learning_path(user_id, assessment_result, study_time)
    print("Generated learning path:")
    print(json.dumps(path, indent=2)) 