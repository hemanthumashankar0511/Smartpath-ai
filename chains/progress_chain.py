from data import db
import json
from datetime import datetime
from typing import List, Dict, Any

def record_progress(user_id: int, completed_items: List[str]):
    """
    Record completed milestones for a user and update the progress table.
    """
    now = datetime.now().isoformat()
    conn = db.get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO progress (user_id, completed_items, last_updated) VALUES (?, ?, ?)",
        (user_id, json.dumps(completed_items), now)
    )
    conn.commit()
    conn.close()

def get_progress(user_id: int) -> Dict[str, Any]:
    """
    Retrieve progress data for a user.
    """
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT completed_items, last_updated FROM progress WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        completed_items = json.loads(row[0])
        last_updated = row[1]
        return {"completed_items": completed_items, "last_updated": last_updated}
    return {"completed_items": [], "last_updated": None}

def calculate_velocity(progress_history: List[Dict[str, Any]]) -> float:
    """
    Calculate learning velocity (milestones per week) from progress history.
    """
    if len(progress_history) < 2:
        return 0.0
    first = datetime.fromisoformat(progress_history[0]['last_updated'])
    last = datetime.fromisoformat(progress_history[-1]['last_updated'])
    total_days = (last - first).days or 1
    total_completed = len(progress_history[-1]['completed_items'])
    return total_completed / (total_days / 7)

def suggest_adjustments(velocity: float, target_velocity: float) -> str:
    """
    Suggest path adjustments based on current and target velocity.
    """
    if velocity < target_velocity * 0.7:
        return "Consider allocating more study time or reducing milestones per week."
    elif velocity > target_velocity * 1.3:
        return "You are progressing faster than planned! Consider adding advanced topics."
    else:
        return "You are on track. Keep going!"

if __name__ == "__main__":
    # Example usage
    user_id = 1
    completed = ["Python Basics", "Control Flow"]
    record_progress(user_id, completed)
    progress = get_progress(user_id)
    print("Current progress:", progress)
    # Simulate progress history for velocity
    history = [
        {"completed_items": ["Python Basics"], "last_updated": "2024-05-01T10:00:00"},
        {"completed_items": ["Python Basics", "Control Flow"], "last_updated": "2024-05-08T10:00:00"}
    ]
    velocity = calculate_velocity(history)
    print(f"Learning velocity: {velocity:.2f} milestones/week")
    print(suggest_adjustments(velocity, target_velocity=1.0)) 