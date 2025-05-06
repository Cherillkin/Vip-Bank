from datetime import datetime, timedelta

from sqlalchemy import func
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.types import TypeDecorator, LargeBinary
from sqlalchemy.orm import Session
from . import schemas, database
from . import models
import os
import bcrypt

import logging

from jose import jwt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

SECRET_KEY = 'my_secret_key'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    logger.warning("ENCRYPTION_KEY not set. Generating a new one (not recommended in production).")
    ENCRYPTION_KEY = Fernet.generate_key().decode()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_client(db: Session, client: schemas.КлиентCreate):
    existing_client = db.query(models.Клиент).filter(models.Клиент.email == client.email).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Клиент с таким email уже существует.")

    role = db.query(models.Роль).filter(models.Роль.id_роли == client.id_роли).first()
    if not role:
        raise HTTPException(status_code=400, detail=f"Роль с ID {client.id_роли} не найдена.")

    hashed_password = hash_password(client.пароль)

    db_client = models.Клиент(
        email=client.email,
        фамилия=client.фамилия,
        имя=client.имя,
        отчество=client.отчество,
        пароль=hashed_password,
        дата_создания=datetime.utcnow(),
        дата_обновление=datetime.utcnow(),
        роль=role
    )

    access_token = create_access_token(data={"sub": db_client.email})
    refresh_token = create_access_token(data={"sub": db_client.email}, expires_delta=timedelta(days=7))

    db_client.access_token = access_token
    db_client.refresh_token = refresh_token
    db.commit()
    db.refresh(db_client)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_client(db: Session, email: str, password: str):
    client = db.query(models.Клиент).filter(models.Клиент.email == email).first()
    if not client:
        return None
    if not verify_password(password, client.пароль):
        return None

    access_token = create_access_token(data={"sub": client.email})
    refresh_token = create_access_token(data={"sub": client.email}, expires_delta=timedelta(days=7))

    client.access_token = access_token
    client.refresh_token = refresh_token
    db.commit()
    db.refresh(client)

    return client

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Роль(роль=role.роль)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def create_street(db: Session, street: schemas.УлицаOut):
    db_street = models.Улица(название_улицы=street.название_улицы)
    db.add(db_street)
    db.commit()
    db.refresh(db_street)
    return db_street

def create_branch(db: Session, branch: schemas.ФилиалOut):
    street = db.query(models.Улица).filter(models.Улица.id_улицы == branch.улица_филиала).first()
    if not street:
        raise HTTPException(status_code=400, detail=f"Улица с ID {branch.улица_филиала} не найдена.")

    db_branch = models.Филиал(
        улица_филиала=branch.улица_филиала,
        дом_филиала=branch.дом_филиала,
        корпус_филиала=branch.корпус_филиала
    )

    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)

    return db_branch

def create_account(db: Session, account: schemas.СчетBase):
    id_client = db.query(models.Клиент).filter(models.Клиент.id_клиента == account.id_клиента).first()
    if not id_client:
        raise HTTPException(status_code=400, detail=f"Клиент с ID {account.id_клиента} не найден.")

    id_branch = db.query(models.Филиал).filter(models.Филиал.id_филиала == account.id_филиала).first()
    if not id_branch:
        raise HTTPException(status_code=400, detail=f"Филиал с ID {account.id_филиала} не найден.")

    id_account_from_type = db.query(models.ВидСчета).filter(models.ВидСчета.id_вида_счета == account.id_вида_счета).first()
    if not id_account_from_type:
        raise HTTPException(status_code=400, detail=f"Вид счета с ID {account.id_вида_счета} не найден.")

    db_account = models.Счет(
        баланс=account.баланс,
        id_клиента=account.id_клиента,
        id_филиала=account.id_филиала,
        id_вида_счета=account.id_вида_счета,
        дата_открытия=datetime.utcnow()
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def create_invest_account(db: Session, invest_account: schemas.ИнвестицииBase):
    client = db.query(models.Клиент).filter(models.Клиент.id_клиента == invest_account.id_клиента).first()
    if not client:
        raise HTTPException(status_code=404, detail=f"Клиент с id {invest_account.id_клиента} не найден")

    account = db.query(models.Счет).filter(models.Счет.id_клиента == invest_account.id_клиента).first()
    if not account:
        raise HTTPException(status_code=404, detail=f"Счёт клиента с id {invest_account.id_клиента} не найден")

    if account.баланс < invest_account.баланс:
        raise HTTPException(status_code=400, detail="Недостаточно средств на основном счёте")

    account.баланс -= invest_account.баланс

    db_invest_account = models.Инвестиции(
        id_клиента=invest_account.id_клиента,
        баланс=invest_account.баланс,
        дата_создания=invest_account.дата_создания,
        статус=invest_account.статус
    )

    db.add(db_invest_account)
    db.commit()
    db.refresh(db_invest_account)

    return db_invest_account

def get_invest_account_by_id(db: Session, invest_account_id: int):
    db_invest_account_id = db.query(models.Инвестиции).filter(models.Инвестиции.id_портфеля == invest_account_id).first()
    if not db_invest_account_id:
        raise HTTPException(status_code=404, detail="Портфель не найден")
    return db_invest_account_id

def get_account_by_id(db: Session, account_id: int):
    db_account = db.query(models.Счет).filter(models.Счет.id_счета == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Счёт не найден")
    return db_account

def create_account_from_type(db: Session, account_from_type: schemas.ВидСчетаBase):
    account_type = db.query(models.ТипСчета).filter(
        models.ТипСчета.id_типа_счета == account_from_type.id_типа_счета
    ).first()

    if not account_type:
        raise HTTPException(status_code=400, detail=f"Тип счета с ID {account_from_type.id_типа_счета} не найден.")

    db_account_from_type = models.ВидСчета(
        название_вида_счета=account_from_type.название_вида_счета,
        тип=account_type
    )

    db.add(db_account_from_type)
    db.commit()
    db.refresh(db_account_from_type)

    return db_account_from_type

def create_interest_rate(db: Session, interest_rate: schemas.ПроцентнаяСтавкаBase):
    db_вид_счета = db.query(models.ВидСчета).filter(
        models.ВидСчета.id_вида_счета == interest_rate.id_вида_счета).first()
    if not db_вид_счета:
        raise HTTPException(status_code=404, detail="Вид счета не найден")

    interest_rate.дата_изменения = datetime.utcnow()

    db_ставка = models.ПроцентнаяСтавка(
        процентная_ставка=interest_rate.процентная_ставка,
        id_вида_счета=interest_rate.id_вида_счета,
        дата_изменения=interest_rate.дата_изменения
    )
    db.add(db_ставка)
    db.commit()
    db.refresh(db_ставка)
    return (db_ставка)

def create_investment_details(db: Session, investment_details: schemas.ДеталиИнвестицийBase):
    id_briefcase = db.query(models.Инвестиции).filter(
        models.Инвестиции.id_портфеля == investment_details.id_портфеля
    ).first()

    if not id_briefcase:
        raise HTTPException(status_code=404, detail=f"Портфель с id {investment_details.id_портфеля} не найден")

    id_type_invest = db.query(models.ТипИнвестиций).filter(
        models.ТипИнвестиций.id_типа_инвестиций == investment_details.id_типа_инвестиций
    ).first()

    if not id_type_invest:
        raise HTTPException(status_code=404, detail=f"Тип инвестиции с id {investment_details.id_типа_инвестиций} не найден")

    total_investments_sum = db.query(func.sum(models.ДеталиИнвестиций.сумма)).filter(
        models.ДеталиИнвестиций.id_портфеля == investment_details.id_портфеля
    ).scalar() or 0

    portfolio_balance = id_briefcase.баланс

    if total_investments_sum + investment_details.сумма > portfolio_balance:
        raise HTTPException(status_code=400, detail="Недостаточно средств для покупки актива")

    db_investment_detail = models.ДеталиИнвестиций(
        id_портфеля=investment_details.id_портфеля,
        id_типа_инвестиций=investment_details.id_типа_инвестиций,
        сумма=investment_details.сумма,
        дата_покупки=investment_details.дата_покупки
    )

    db.add(db_investment_detail)
    db.commit()
    db.refresh(db_investment_detail)

    calculate_and_create_yield(db, investment_details.id_портфеля)

    return db_investment_detail

def get_investment_details_by_briefcase_id(db: Session, briefcase_id: int):
    details = db.query(models.ДеталиИнвестиций).filter(
        models.ДеталиИнвестиций.id_портфеля == briefcase_id
    ).all()

    if not details:
        raise HTTPException(status_code=404, detail=f"Деталей инвестиций для портфеля с id {briefcase_id} не найдены")

    return details

def delete_account_type_by_id(db: Session, id_вида_счета: int):
    account_type = db.query(models.ВидСчета).filter(models.ВидСчета.id_вида_счета == id_вида_счета).first()
    if not account_type:
        raise HTTPException(status_code=404, detail=f"Вид счета с ID {id_вида_счета} не найден.")

    db.delete(account_type)
    db.commit()

    return {"message": f"Вид счета с ID {id_вида_счета} успешно удален."}

def get_clients(db: Session):
    return db.query(models.Клиент).all()

def get_client_by_id(db: Session, client_id: int):
    return db.query(models.Клиент).filter(models.Клиент.id_клиента == client_id).first()

def get_roles(db: Session):
    return db.query(models.Роль).all()

def get_operations(db: Session):
    return db.query(models.Операция).all()

def get_street(db: Session):
    return db.query(models.Улица).all()

def get_account_type(db: Session):
    return db.query(models.ТипСчета).all()

def get_account_from_type(db: Session):
    return db.query(models.ВидСчета).all()

def get_interest_rates(db: Session):
    return db.query(models.ПроцентнаяСтавка).all()

def get_all_branches(db: Session):
    return db.query(models.Филиал).all()

def get_id_interest_rate(db: Session, id_процентной_ставки: int):
    return db.query(models.ПроцентнаяСтавка).filter(models.ПроцентнаяСтавка.id_процентной_ставки == id_процентной_ставки).first()

def get_all_type_invest(db: Session):
    return db.query(models.ТипИнвестиций).all()

def update_дата_изменения(db: Session, id_процентной_ставки: int):
    db_rate = db.query(models.ПроцентнаяСтавка).filter(models.ПроцентнаяСтавка.id_процентной_ставки == id_процентной_ставки).first()
    if db_rate:
        db_rate.дата_изменения = datetime.utcnow()
        db.commit()
        db.refresh(db_rate)
    return db_rate

def transfer_funds(id_sender: int, id_recipient: int, amount: int, db):
    sender = db.query(models.Счет).filter(models.Счет.id_клиента == id_sender).first()
    recipient = db.query(models.Счет).filter(models.Счет.id_клиента == id_recipient).first()

    if not sender or not recipient:
        raise HTTPException(status_code=404, detail="Один из клиентов не найден")

    if sender.баланс < amount:  # Decrypted balance is used directly
        raise HTTPException(status_code=400, detail="Недостаточно средств на счете отправителя")

    sender.баланс -= amount  # Update triggers encryption
    recipient.баланс += amount  # Update triggers encryption

    operation_translation = db.query(models.Операция).filter(models.Операция.id_операции == 3).first()

    if not operation_translation:
        raise HTTPException(status_code=404, detail="Операция с типом 'перевод' не найдена")

    operation_transmitter = models.БанковскаяОперация(
        id_счета=sender.id_счета,
        сумма=-amount,
        id_операции=operation_translation.id_операции
    )

    operation_recipient = models.БанковскаяОперация(
        id_счета=recipient.id_счета,
        сумма=amount,
        id_операции=operation_translation.id_операции
    )

    db.add(operation_transmitter)
    db.add(operation_recipient)

    db.commit()
    db.refresh(sender)
    db.refresh(recipient)

def cash_withdrawal(id_client: int, amount: int, db):
    account = db.query(models.Счет).filter(models.Счет.id_клиента == id_client).first()

    if not account:
        raise HTTPException(status_code=404, detail="Данный клиент не найден")

    if account.баланс < amount:  # Decrypted balance is used directly
        raise HTTPException(status_code=404, detail="Недостаточно средств для снятия наличных")

    account.баланс -= amount  # Update triggers encryption

    operation_translation = db.query(models.Операция).filter(models.Операция.id_операции == 2).first()

    if not operation_translation:
        raise HTTPException(status_code=404, detail="Операция с типом 'снятие' не найдена")

    operation_client_id = models.БанковскаяОперация(
        id_счета=account.id_счета,
        сумма=-amount,
        id_операции=operation_translation.id_операции
    )

    db.add(operation_client_id)

    db.commit()
    db.refresh(account)

def cash_replenishment(id_client: int, amount: int, db):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Сумма должна быть положительной")

    account = db.query(models.Счет).filter(models.Счет.id_клиента == id_client).first()

    if not account:
        raise HTTPException(status_code=404, detail="Данный клиент не найден")

    account.баланс += amount  # Update triggers encryption

    operation_translation = db.query(models.Операция).filter(models.Операция.id_операции == 1).first()

    if not operation_translation:
        raise HTTPException(status_code=404, detail="Операция с типом 'пополнение' не найдена")

    operation_client_id = models.БанковскаяОперация(
        id_счета=account.id_счета,
        сумма=amount,
        id_операции=operation_translation.id_операции
    )

    db.add(operation_client_id)

    db.commit()
    db.refresh(account)

def calculate_and_create_yield(db: Session, briefcase_id: int):
    total_sum = db.query(func.sum(models.ДеталиИнвестиций.сумма)).filter(
        models.ДеталиИнвестиций.id_портфеля == briefcase_id
    ).scalar()

    if total_sum is None:
        raise HTTPException(status_code=404, detail=f"Нет инвестиций для портфеля с id {briefcase_id}")

    yield_entry = models.ДоходностьИнвестиций(
        id_портфеля=briefcase_id,
        доходность=total_sum,
        дата_обновления=datetime.utcnow()
    )

    db.add(yield_entry)
    db.commit()
    db.refresh(yield_entry)

    return yield_entry

def get_yield_by_briefcase_id(db: Session, briefcase_id: int):
    yield_entry = db.query(models.ДоходностьИнвестиций).filter(
        models.ДоходностьИнвестиций.id_портфеля == briefcase_id
    ).order_by(models.ДоходностьИнвестиций.дата_обновления.desc()).first()

    if not yield_entry:
        raise HTTPException(status_code=404, detail=f"Доходность для портфеля с id {briefcase_id} не найдена")

    return yield_entry

class CRUDClient:
    def update_client(self, db: Session, client_id: int, client_update: schemas.КлиентUpdate):
        db_client = db.query(models.Клиент).filter(models.Клиент.id_клиента == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail="Клиент не найден.")

        if client_update.email is not None:
            db_client.email = client_update.email
        if client_update.фамилия is not None:
            db_client.фамилия = client_update.фамилия
        if client_update.имя is not None:
            db_client.имя = client_update.имя
        if client_update.отчество is not None:
            db_client.отчество = client_update.отчество
        if client_update.пароль is not None:
            db_client.пароль = hash_password(client_update.пароль)
        if client_update.id_роли is not None:
            db_client.id_роли = client_update.id_роли

        db_client.дата_обновления = datetime.utcnow()

        db.commit()
        db.refresh(db_client)

        return db_client

class EncryptedBalance(TypeDecorator):
    impl = LargeBinary  # Store encrypted data as binary
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        try:
            value_str = str(value)
            nonce = os.urandom(12)
            aesgcm = AESGCM(ENCRYPTION_KEY.encode()[:32])
            encrypted = aesgcm.encrypt(nonce, value_str.encode(), None)
            return nonce + encrypted
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        try:
            nonce = value[:12]
            encrypted = value[12:]
            aesgcm = AESGCM(ENCRYPTION_KEY.encode()[:32])
            decrypted = aesgcm.decrypt(nonce, encrypted, None)
            return int(decrypted.decode())
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise