from fastapi import APIRouter, HTTPException, status
from typing import Annotated

from database import SessionDep
from schemas.books import SBook, SBookAdd
from repository.book import BookRepository  # Импортируем наш новый класс

router = APIRouter(prefix="/books", tags=["Книги"])

@router.post("", response_model=SBook)
async def create_book(
    book: SBookAdd,
    session: SessionDep,
):
    # Вся логика сохранения ушла в репозиторий.
    # Роутер просто передает данные и ждет результат.
    book_model = await BookRepository.add_one(book, session)
    return book_model

@router.get("", response_model=list[SBook])
async def get_books(
    session: SessionDep,
):
    # Роутер не знает, как выполняется поиск (SQL? Файл? API?).
    # Ему нужен просто список задач.
    books = await BookRepository.find_all(session)
    return books


@router.get("/{id}", response_model=list[SBook])
async def get_book_by_id(
    session: SessionDep,
    id: int
):
    # Роутер не знает, как выполняется поиск (SQL? Файл? API?).
    # Ему нужен просто список задач.
    book = await BookRepository.get_book_by_id(session, id)
    if book: 
        return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail= "Книга не найдена"
    )