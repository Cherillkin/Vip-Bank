from sqlalchemy import Column, DateTime, func
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class РольBase(BaseModel):
    роль: str

class RoleCreate(BaseModel):
    роль: str

    model_config = {
        "from_attributes": True
    }

class РольOut(РольBase):
    id_роли: int

    model_config = {
        "from_attributes": True
    }


class ТипСчетаBase(BaseModel):
    название_типа_счета: str

class ТипСчетаOut(ТипСчетаBase):
    id_типа_счета: int

    model_config = {
        "from_attributes": True
    }

class ПроцентнаяСтавкаBase(BaseModel):
    процентная_ставка: int
    id_вида_счета: int
    дата_изменения: datetime

class ПроцентнаяСтавкаOut(ПроцентнаяСтавкаBase):
    id_процентной_ставки: int

    model_config = {
        "from_attributes": True
    }

class ВидСчетаBase(BaseModel):
    название_вида_счета: str
    id_типа_счета: int

class ВидСчетаOut(ВидСчетаBase):
    id_вида_счета: int
    тип: ТипСчетаOut
    процентные_ставки: List[ПроцентнаяСтавкаOut] = []

    model_config = {
        "from_attributes": True
    }

class ОперацияBase(BaseModel):
    название_операции: str

class ОперацияOut(ОперацияBase):
    id_операции: int

    model_config = {
        "from_attributes": True
    }

class БанковскаяОперацияBase(BaseModel):
    сумма: int
    id_счета: int
    id_операции: int

class БанковскаяОперацияOut(БанковскаяОперацияBase):
    id_банковской_операции: int
    операция: ОперацияOut
    дата_операции: datetime

    model_config = {
        "from_attributes": True
    }

class СчетBase(BaseModel):
    баланс: int
    id_клиента: int
    id_филиала: int
    id_вида_счета: int
    дата_открытия: datetime
    id_счета_источника: Optional[int] = None

class СчетOut(СчетBase):
    id_счета: int
    вид: ВидСчетаOut
    операции: List[БанковскаяОперацияOut]

    model_config = {
        "from_attributes": True
    }

class КлиентBase(BaseModel):
    email: Optional[str]
    фамилия: Optional[str]
    имя: Optional[str]
    отчество: Optional[str]
    пароль: Optional[str]
    id_роли: Optional[int]
    дата_создания: Optional[datetime] = None
    дата_обновления: Optional[datetime] = None

class КлиентCreate(КлиентBase):
    pass

class КлиентUpdate(BaseModel):
    email: Optional[str] = None
    фамилия: Optional[str] = None
    имя: Optional[str] = None
    отчество: Optional[str] = None
    пароль: Optional[str] = None
    id_роли: Optional[int] = None


class КлиентLogin(BaseModel):
    email: EmailStr
    пароль: str


class КлиентOut(КлиентBase):
    id_клиента: int
    дата_создания: Optional[datetime] = None
    дата_обновления: Optional[datetime] = None
    роль: РольOut
    счета: List[СчетOut]

    model_config = {
        "from_attributes": True
    }

class ФилиалBase(BaseModel):
    улица_филиала: int
    дом_филиала: int
    корпус_филиала: int

class ФилиалOut(ФилиалBase):

    model_config = {
        "from_attributes": True
    }

class ТипИнвестицийBase(BaseModel):
    название_типа: str

class ТипИнвестицийOut(ТипИнвестицийBase):
    id_типа_инвестиций: int

    model_config = {
        "from_attributes": True
    }


class ДеталиИнвестицийBase(BaseModel):
    id_портфеля: int
    id_типа_инвестиций: int
    сумма: int
    дата_покупки: datetime

class ДеталиИнвестицийOut(ДеталиИнвестицийBase):
    id_детали: int

    model_config = {
        "from_attributes": True
    }

class ДоходностьИнвестицийBase(BaseModel):
    доходность: float
    дата_обновления: datetime

class ДоходностьИнвестицийOut(ДоходностьИнвестицийBase):
    id_доходности: int

    model_config = {
        "from_attributes": True
    }


class ИнвестицииBase(BaseModel):
    id_клиента: int
    баланс: int
    дата_создания: datetime = Column(DateTime, default=func.now())
    статус: str

class ИнвестицииOut(ИнвестицииBase):
    id_портфеля: int
    баланс: int
    дата_создания: datetime = Column(DateTime, default=func.now())
    статус: str

    model_config = {
        "from_attributes": True
    }

class УлицаBase(BaseModel):
    название_улицы: str

class УлицаCreate(УлицаBase):
    pass

class УлицаOut(УлицаBase):
    id_улицы: int

    model_config = {
        "from_attributes": True
    }

class TokenData(BaseModel):
    email: str
    id: int
    role: int