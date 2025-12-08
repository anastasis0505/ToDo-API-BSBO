from datetime import date, datetime
from typing import Optional

def calculate_urgency(deadline_at: Optional[date]) -> bool:
    """Определяет срочность: True если до дедлайна <= 3 дня"""
    if deadline_at is None:
        return False
    
    today = date.today()
    days_until_deadline = (deadline_at - today).days
    return days_until_deadline <= 3

def calculate_days_until_deadline(deadline_at: Optional[date]) -> Optional[int]:
    """Рассчитывает дни до дедлайна"""
    if deadline_at is None:
        return None
    
    today = date.today()
    return (deadline_at - today).days

def determine_quadrant(is_important: bool, deadline_at: Optional[date]) -> str:
    """Определяет квадрант на основе важности и дедлайна"""
    is_urgent = calculate_urgency(deadline_at)
    
    if is_important and is_urgent:
        return "Q1"
    elif is_important and not is_urgent:
        return "Q2"
    elif not is_important and is_urgent:
        return "Q3"
    else:
        return "Q4"