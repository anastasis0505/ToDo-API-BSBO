# routers/stats.py
from fastapi import APIRouter
from typing import Dict, Any
from database import tasks_db

router = APIRouter(
    prefix="/stats",  # ПРЕФИКС /stats как в задании!
    tags=["stats"],
    responses={404: {"description": "Stats not found"}},
)

@router.get("/tasks/state")
async def get_tasks_stats() -> Dict[str, Any]:
    """
    Получить статистику по задачам
    """
    # Общее количество задач
    total_tasks = len(tasks_db)
    
    # Подсчет по квадрантам
    by_quadrant = {
        "Q1": 0,
        "Q2": 0,
        "Q3": 0,
        "Q4": 0
    }
    
    # Подсчет по статусу
    by_status = {
        "completed": 0,
        "pending": 0
    }
    
    # Подсчитываем статистику
    for task in tasks_db:
        # Подсчет по квадрантам
        quadrant = task["quadrant"]
        if quadrant in by_quadrant:
            by_quadrant[quadrant] += 1
        
        # Подсчет по статусу
        if task["completed"]:
            by_status["completed"] += 1
        else:
            by_status["pending"] += 1
    
    return {
        "total_tasks": total_tasks,
        "by_quadrant": by_quadrant,
        "by_status": by_status,
        "percentage_completed": round((by_status["completed"] / total_tasks * 100), 2) if total_tasks > 0 else 0
    }
