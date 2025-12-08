# routers/tasks.py
from fastapi import APIRouter, HTTPException, Response, status, Query
from typing import List, Optional
from datetime import datetime

from schemas import TaskCreate, TaskUpdate, TaskResponse
from database import tasks_db

router = APIRouter(
    prefix="/tasks",  # ДОБАВЛЯЕМ ПРЕФИКС здесь!
    tags=["tasks"],
    responses={404: {"description": "Task not found"}},
)

# Вспомогательная функция для определения квадранта
def determine_quadrant(is_important: bool, is_urgent: bool) -> str:
    if is_important and is_urgent:
        return "Q1"
    elif is_important and not is_urgent:
        return "Q2"
    elif not is_important and is_urgent:
        return "Q3"
    else:
        return "Q4"

# GET все задачи
@router.get("/", response_model=List[TaskResponse])
async def get_all_tasks():
    """
    Получить все задачи
    """
    return tasks_db

# GET задача по ID
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(task_id: int):
    """
    Получить задачу по ID
    """
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с ID {task_id} не найдена"
        )
    return task

# POST создание задачи
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate):
    """
    Создать новую задачу
    """
    # Определяем квадрант
    quadrant = determine_quadrant(task.is_important, task.is_urgent)
    
    # Генерируем новый ID
    new_id = max([t["id"] for t in tasks_db], default=0) + 1
    
    # Создаём новую задачу
    new_task = {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "is_important": task.is_important,
        "is_urgent": task.is_urgent,
        "quadrant": quadrant,
        "completed": False,
        "created_at": datetime.now(),
        "completed_at": None
    }
    
    # Добавляем в "базу данных"
    tasks_db.append(new_task)
    
    return new_task

# PUT обновление задачи
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, task_update: TaskUpdate):
    """
    Обновить задачу
    """
    # Ищем задачу по ID
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    # Получаем только переданные поля
    update_data = task_update.model_dump(exclude_unset=True)
    
    # Обновляем поля
    for field, value in update_data.items():
        task[field] = value
    
    # Пересчитываем квадрант, если изменились важность или срочность
    if "is_important" in update_data or "is_urgent" in update_data:
        task["quadrant"] = determine_quadrant(
            task.get("is_important", False),
            task.get("is_urgent", False)
        )
    
    return task

# PATCH отметка задачи как выполненной
@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int):
    """
    Отметить задачу как выполненную
    """
    # Ищем задачу по ID
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    # Обновляем статус
    task["completed"] = True
    task["completed_at"] = datetime.now()
    
    return task

# DELETE удаление задачи
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    """
    Удалить задачу
    """
    # Ищем задачу по ID
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    
    if not task:
        raise HTTPException(
            status_code=404,
            detail=f"Задача с ID {task_id} не найдена"
        )
    
    # Удаляем задачу
    tasks_db.remove(task)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# GET задачи по квадранту
@router.get("/quadrant/{quadrant}", response_model=List[TaskResponse])
async def get_tasks_by_quadrant(quadrant: str):
    """
    Получить задачи по квадранту
    """
    if quadrant not in ["Q1", "Q2", "Q3", "Q4"]:
        raise HTTPException(
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4"
        )
    
    filtered_tasks = [task for task in tasks_db if task["quadrant"] == quadrant]
    return filtered_tasks

# GET задачи по статусу
@router.get("/status/{status}", response_model=List[TaskResponse])
async def get_tasks_by_status(status: str):
    """
    Получить задачи по статусу
    """
    if status not in ["completed", "pending"]:
        raise HTTPException(
            status_code=400,
            detail="Неверный статус. Используйте: completed или pending"
        )
    
    is_completed = (status == "completed")
    filtered_tasks = [task for task in tasks_db if task["completed"] == is_completed]
    return filtered_tasks

# GET поиск задач
@router.get("/search", response_model=List[TaskResponse])
async def search_tasks(q: str = Query(..., min_length=1, description="Поисковый запрос")):
    """
    Поиск задач
    """
    search_results = []
    for task in tasks_db:
        if (q.lower() in task["title"].lower() or 
            (task["description"] and q.lower() in task["description"].lower())):
            search_results.append(task)
    
    if not search_results:
        raise HTTPException(
            status_code=404,
            detail=f"Задачи по запросу '{q}' не найдены"
        )
    
    return search_results
