from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BooksModel
from schemas.books import SBookAdd


class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd, session: AsyncSession) -> BooksModel:
        # 1. Превращаем данные из Pydantic в словарь
        book_dict = data.model_dump()
        # 2. Создаем объект модели
        book = BooksModel(**book_dict) 
        # 3. Добавляем и сохраняем
        session.add(book)
        await session.commit()
        await session.refresh(book)
        # 4. Возвращаем созданный объект
        return book

    @classmethod
    async def find_all(cls, session: AsyncSession):
        # 1. Готовим запрос
        query = select(BooksModel)
        # 2. Выполняем
        result = await session.execute(query)
        # 3. Возвращаем список объектов
        books_models = result.scalars().all()
        return books_models
    
    @classmethod
    async def get_book_by_id(cls, session: AsyncSession, book_id: int):
        # 1. Готовим запрос
        query = select(BooksModel).where(BooksModel.id == book_id)
        # 2. Выполняем
        result = await session.execute(query)
        # # 3. Возвращаем список объектов
        return result.one_or_none()
    
    @classmethod
    async def update_book(cls, book_id: int, book: SBookAdd, session: AsyncSession):
        stmt = select(BooksModel).where(BooksModel.id == book_id)
        book_db = await session.scalars(stmt)
        if book_db.first():
            book_data = book.model_dump()
            book_data["id"] = book_id
            stmt = update(BooksModel).where(BooksModel.id == book_id).values(book_data)
            await session.execute(stmt)
            await session.commit()
            return book_data

    @classmethod
    async def delete_book(cls, book_id: int, session: AsyncSession):
        stmt = select(BooksModel).where(BooksModel.id == book_id)
        result = await session.scalars(stmt)
        if result.first():
            await session.execute(delete(BooksModel).where(BooksModel.id == book_id))
            await session.commit()
            return True