# main.py
from fastapi import FastAPI
from routers.tasks import router as tasks_router
from routers.stats import router as stats_router

app = FastAPI(
    title="ToDo Matrix API",
    description="API для управления задачами с использованием матрицы Эйзенхауэра",
    version="1.0.0",
    contact={
        "name": "Анастасия",
    }
)

# Подключаем роутеры с префиксом /api/v1
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(stats_router, prefix="/api/v1")  # будет /api/v1/stats/tasks/state

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Привет, студент!",
        "api_title": app.title,
        "api_description": app.description,
        "api_version": app.version,
        "api_author": app.contact["name"],
        "documentation": "/docs",
        "openapi": "/openapi.json"
    }

@app.get("/api/v1/")
async def api_v1_root() -> dict:
    return {
        "message": "Todo Matrix API v1",
        "documentation": "/docs",
        "endpoints": {
            "tasks": {
                "get_all": "GET /api/v1/tasks",
                "create": "POST /api/v1/tasks",
                "get_by_id": "GET /api/v1/tasks/{id}",
                "update": "PUT /api/v1/tasks/{id}",
                "delete": "DELETE /api/v1/tasks/{id}",
                "complete": "PATCH /api/v1/tasks/{id}/complete",
                "by_quadrant": "GET /api/v1/tasks/quadrant/{quadrant}",
                "by_status": "GET /api/v1/tasks/status/{status}",
                "search": "GET /api/v1/tasks/search?q={query}"
            },
            "stats": {
                "tasks_state": "GET /api/v1/stats/tasks/state"  # ИЗМЕНЕНИЕ!
            }
        }
    }
