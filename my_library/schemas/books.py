from pydantic import BaseModel, Field, ConfigDict

# 1. Базовый класс (общие поля)
class SBookBase(BaseModel):
    title: str
    author: str
    year: int
    pages: int = Field(gt=10)
    is_read: bool = False

# 2. Класс для создания (ничего не добавляет, просто копирует базу)
class SBookAdd(SBookBase):
    pass

# 3. Класс для чтения (добавляет id)
class SBook(SBookBase):
    id: int

    # 2. Включаем поддержку ORM
    model_config = ConfigDict(from_attributes=True)