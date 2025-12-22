from sqlalchemy import select
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