from contextlib import asynccontextmanager
from database import engine, Model # Импортируем из database.py
from models.books import BooksModel
from fastapi import FastAPI
import uvicorn as uvicorn
from routers.books import router as books_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- КОД ПРИ СТАРТЕ ---
    # Мы обращаемся к движку и просим создать все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    
    print("База данных готова к работе")
    
    yield  # Разделяет старт и выключение
    
    # --- КОД ПРИ ВЫКЛЮЧЕНИИ ---
    print("Выключение сервера")

# Передаем lifespan в приложение
app = FastAPI(lifespan=lifespan)
app.include_router(books_router)


if __name__ == "__main__":
    uvicorn.run("main:app", 
                host="127.0.0.1",
                port=8000,
                reload=True)