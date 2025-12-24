from fastapi import APIRouter, HTTPException, status
from typing import Annotated

from database import SessionDep
from schemas.books import SBook, SBookAdd
from repository.book import BookRepository  # Импортируем наш новый класс

router = APIRouter(prefix="/books", tags=["Книги"])

@router.post("", response_model=SBook)
async def create_book(book: SBookAdd, session: SessionDep):
    # Вся логика сохранения ушла в репозиторий.
    # Роутер просто передает данные и ждет результат.
    book_model = await BookRepository.add_one(book, session)
    return book_model

@router.get("", response_model=list[SBook])
async def get_books(session: SessionDep):
    # Роутер не знает, как выполняется поиск (SQL? Файл? API?).
    # Ему нужен просто список задач.
    books = await BookRepository.find_all(session)
    return books


@router.get("/{id:int}", response_model=list[SBook])
async def get_book_by_id(session: SessionDep, id: int):
    # Роутер не знает, как выполняется поиск (SQL? Файл? API?).
    # Ему нужен просто список задач.
    book = await BookRepository.get_book_by_id(session, id)
    if book: 
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Книга не найдена")


@router.put("/{id:int}", response_model=SBook)
async def update_book(session: SessionDep, id: int, book: SBookAdd):
    book = await BookRepository.update_book(id, book, session)
    if book:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")


@router.delete("/{id:int}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: int, session: SessionDep):
    book = await BookRepository.delete_book(id, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")