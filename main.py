from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from database import init_db, get_async_session
from routers import tasks, stats

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код ДО yield выполняется при ЗАПУСКЕ
    print("Starting application...")
    print("Initializing database...")
    
    # Создаем таблицы (если их нет)
    await init_db()
    print("Application ready!")
    
    yield  # Здесь приложение работает
    
    # Код ПОСЛЕ yield выполняется при ОСТАНОВКЕ
    print("Stopping application...")

app = FastAPI(
    title="ToDo API",
    description="API for task management using Eisenhower Matrix",
    version="2.0.0",
    contact={
        "name": "Anastasia",
    },
    lifespan=lifespan
)

# Подключаем роутеры с новым префиксом
app.include_router(tasks.router, prefix="/api/v2")
app.include_router(stats.router, prefix="/api/v2")

@app.get("/")
async def read_root() -> dict:
    return {
        "message": "Task Manager API - Eisenhower Matrix",
        "version": "2.0.0",
        "database": "PostgreSQL (Supabase)",
        "features": "Deadlines, automatic urgency detection",
        "docs": "/docs",
        "redoc": "/redoc",
    }

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_async_session)) -> dict:
    """
    API health check and database connection test
    """
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "version": "2.0.0"
    }
