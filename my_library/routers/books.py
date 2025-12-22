from fastapi import APIRouter
from typing import Annotated

from database import SessionDep
from schemas.books import SBook, SBookAdd
from repository.book import BookRepository  # Импортируем наш новый класс

router = APIRouter(prefix="/books", tags=["Книги"])

@router.post("", response_model=SBook)
async def create_book(
    task: SBookAdd,
    session: SessionDep,
):
    # Вся логика сохранения ушла в репозиторий.
    # Роутер просто передает данные и ждет результат.
    task_model = await BookRepository.add_one(task, session)
    return task_model

@router.get("", response_model=list[SBook])
async def get_books(
    session: SessionDep,
):
    # Роутер не знает, как выполняется поиск (SQL? Файл? API?).
    # Ему нужен просто список задач.
    tasks = await BookRepository.find_all(session)
    return tasks