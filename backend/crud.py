from datetime import datetime, timedelta, time

from fastapi.security import OAuth2PasswordBearer
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from sqlalchemy.types import TypeDecorator, LargeBinary
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from . import schemas, database
import os
import re
import bcrypt

import logging

from jose import jwt, JWTError

from .models.user import Клиент, Роль
from .models.street import Улица
from .models.branch import Филиал
from .models.account import Счет
from .models.account_from_type import ВидСчета
from .models.account_type import ТипСчета
from .models.interest_rage import ПроцентнаяСтавка
from .models.bank_operation import БанковскаяОперация
from .models.operation import Операция

from .schemas import TokenData

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

def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Пароль должен содержать минимум 8 символов.")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну заглавную букву.")
    if not re.search(r"[a-z]", password):
        raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну строчную букву.")
    if not re.search(r"\d", password):
        raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы одну цифру.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(status_code=400, detail="Пароль должен содержать хотя бы один специальный символ.")

def create_admin_or_operator(db: Session, client: schemas.КлиентCreate):
    existing_client = db.query(Клиент).filter(Клиент.email == client.email).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует.")

    role = db.query(Роль).filter(Роль.id_роли == client.id_роли).first()
    if not role:
        raise HTTPException(status_code=400, detail="Роль не найдена.")

    validate_password(client.пароль)
    hashed_password = hash_password(client.пароль)

    try:
        db_client = Клиент(
            email=client.email,
            фамилия=client.фамилия,
            имя=client.имя,
            отчество=client.отчество,
            пароль=hashed_password,
            дата_создания=datetime.utcnow(),
            дата_обновление=datetime.utcnow(),
            роль=role
        )

        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании пользователя: {str(e)}")

def create_client(db: Session, client: schemas.КлиентCreate):
    existing_client = db.query(Клиент).filter(Клиент.email == client.email).first()
    if existing_client:
        raise HTTPException(status_code=400, detail="Клиент с таким email уже существует.")

    role = db.query(Роль).filter(Роль.id_роли == client.id_роли).first()
    if not role:
        raise HTTPException(status_code=400, detail=f"Роль с ID {client.id_роли} не найдена.")

    validate_password(client.пароль)

    hashed_password = hash_password(client.пароль)

    try:
        db_client = Клиент(
            email=client.email,
            фамилия=client.фамилия,
            имя=client.имя,
            отчество=client.отчество,
            пароль=hashed_password,
            дата_создания=datetime.utcnow(),
            дата_обновление=datetime.utcnow(),
            роль=role
        )

        db.add(db_client)
        db.flush()

        create_user_sql = text(f'CREATE USER "{client.email}" WITH PASSWORD \'{client.пароль}\'')
        grant_role_sql = text(f'GRANT rls_user TO "{client.email}"')

        db.execute(create_user_sql)
        db.execute(grant_role_sql)

        access_token = create_access_token(data={"sub": db_client.email})
        refresh_token = create_access_token(data={"sub": db_client.email}, expires_delta=timedelta(days=7))

        db_client.access_token = access_token
        db_client.refresh_token = refresh_token

        db.commit()
        db.refresh(db_client)
        return db_client

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Ошибка при создании клиента: {str(e)}")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_client(db: Session, email: str, password: str):
    client = db.query(Клиент).filter(Клиент.email == email).first()
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
    db_role = Роль(роль=role.роль)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def create_street(db: Session, street: schemas.УлицаOut):
    db_street = Улица(название_улицы=street.название_улицы)
    db.add(db_street)
    db.commit()
    db.refresh(db_street)
    return db_street

def create_branch(db: Session, branch: schemas.ФилиалOut):
    street = db.query(Улица).filter(Улица.id_улицы == branch.улица_филиала).first()
    if not street:
        raise HTTPException(status_code=400, detail=f"Улица с ID {branch.улица_филиала} не найдена.")

    db_branch = Филиал(
        улица_филиала=branch.улица_филиала,
        дом_филиала=branch.дом_филиала,
        корпус_филиала=branch.корпус_филиала
    )

    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)

    return db_branch

def create_account(db: Session, account: schemas.СчетBase):
    if account.баланс < 0:
        raise HTTPException(status_code=400, detail="Баланс не может быть отрицательным.")

    client = db.query(Клиент).filter(Клиент.id_клиента == account.id_клиента).first()
    if not client:
        raise HTTPException(status_code=400, detail=f"Клиент с ID {account.id_клиента} не найден.")

    branch = db.query(Филиал).filter(Филиал.id_филиала == account.id_филиала).first()
    if not branch:
        raise HTTPException(status_code=400, detail=f"Филиал с ID {account.id_филиала} не найден.")

    account_type = db.query(ВидСчета).filter(ВидСчета.id_вида_счета == account.id_вида_счета).first()
    if not account_type:
        raise HTTPException(status_code=400, detail=f"Вид счета с ID {account.id_вида_счета} не найден.")

    type_id = account_type.id_типа_счета

    if type_id == 1:
        existing_credit = (
            db.query(Счет)
            .filter(
                Счет.id_клиента == account.id_клиента,
                Счет.вид.has(id_типа_счета=1)
            )
            .first()
        )
        if existing_credit:
            raise HTTPException(status_code=400, detail="Нельзя открыть более одного кредитного счёта.")

    if type_id == 2:
        if account.id_счета_источника is None:
            raise HTTPException(status_code=400, detail="Для открытия вклада укажите счёт-источник средств.")

        source_account = db.query(Счет).filter(Счет.id_счета == account.id_счета_источника).first()

        if not source_account or source_account.id_клиента != account.id_клиента:
            raise HTTPException(status_code=400, detail="Счёт-источник не найден или не принадлежит клиенту.")

        source_type = source_account.вид.id_типа_счета
        if source_type in [1, 2, 3]:
            raise HTTPException(status_code=400, detail="Нельзя перевести средства с выбранного счёта.")

        if source_account.баланс < account.баланс:
            raise HTTPException(status_code=400, detail="Недостаточно средств на счёте-источнике.")

        source_account.баланс -= account.баланс

        if account.id_счета_источника is None:
            raise HTTPException(status_code=400,
                                detail="Для открытия инвестиционного счета укажите счёт-источник средств.")

        source_account = db.query(Счет).filter(Счет.id_счета == account.id_счета_источника).first()
        if not source_account or source_account.id_клиента != account.id_клиента:
            raise HTTPException(status_code=400, detail="Счёт-источник не найден или не принадлежит клиенту.")

        source_type = source_account.вид.id_типа_счета
        if source_type in [1, 2, 3]:
            raise HTTPException(status_code=400, detail="Нельзя перевести средства с выбранного счёта.")

        if source_account.баланс < account.баланс:
            raise HTTPException(status_code=400, detail="Недостаточно средств на счёте-источнике.")

        source_account.баланс -= account.баланс

    new_account = Счет(
        баланс=account.баланс,
        id_клиента=account.id_клиента,
        id_филиала=account.id_филиала,
        id_вида_счета=account.id_вида_счета,
        дата_открытия=datetime.utcnow(),
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

def get_accounts_by_client_id(db: Session, client_id: int):
    return db.query(Счет).options(
        joinedload(Счет.вид).joinedload(ВидСчета.тип),
        joinedload(Счет.вид).joinedload(ВидСчета.процентные_ставки),
        joinedload(Счет.операции).joinedload(БанковскаяОперация.операция)
    ).filter(Счет.id_клиента == client_id).all()

def get_account_by_id(db: Session, account_id: int):
    db_account = db.query(Счет).filter(Счет.id_счета == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Счёт не найден")
    return db_account

def get_card_operations_by_account(
    db: Session,
    account_id: int,
    start_date: datetime,
    end_date: datetime
):
    account = db.query(Счет).join(ВидСчета).join(ТипСчета).filter(
        Счет.id_счета == account_id,
        ТипСчета.id_типа_счета == 4
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Карта с таким ID не найдена или не является карточной.")

    operations = db.query(БанковскаяОперация).filter(
        БанковскаяОперация.id_счета == account_id,
        БанковскаяОперация.дата_операции >= start_date,
        БанковскаяОперация.дата_операции <= end_date
    ).all()

    return operations

def get_all_operations_by_account(db: Session, account_id: int):
    return db.query(БанковскаяОперация).filter(
        БанковскаяОперация.id_счета == account_id
    ).all()

def create_account_from_type(db: Session, account_from_type: schemas.ВидСчетаBase):
    account_type = db.query(ТипСчета).filter(
        ТипСчета.id_типа_счета == account_from_type.id_типа_счета
    ).first()

    if not account_type:
        raise HTTPException(status_code=400, detail=f"Тип счета с ID {account_from_type.id_типа_счета} не найден.")

    db_account_from_type = ВидСчета(
        название_вида_счета=account_from_type.название_вида_счета,
        тип=account_type
    )

    db.add(db_account_from_type)
    db.commit()
    db.refresh(db_account_from_type)

    return db_account_from_type

def create_interest_rate(db: Session, interest_rate: schemas.ПроцентнаяСтавкаBase):
    db_вид_счета = db.query(ВидСчета).filter(
        ВидСчета.id_вида_счета == interest_rate.id_вида_счета).first()
    if not db_вид_счета:
        raise HTTPException(status_code=404, detail="Вид счета не найден")

    interest_rate.дата_изменения = datetime.utcnow()

    db_ставка = ПроцентнаяСтавка(
        процентная_ставка=interest_rate.процентная_ставка,
        id_вида_счета=interest_rate.id_вида_счета,
        дата_изменения=interest_rate.дата_изменения
    )
    db.add(db_ставка)
    db.commit()
    db.refresh(db_ставка)
    return (db_ставка)

def delete_account_type_by_id(db: Session, id_вида_счета: int):
    account_type = db.query(ВидСчета).filter(ВидСчета.id_вида_счета == id_вида_счета).first()
    if not account_type:
        raise HTTPException(status_code=404, detail=f"Вид счета с ID {id_вида_счета} не найден.")

    db.delete(account_type)
    db.commit()

    return {"message": f"Вид счета с ID {id_вида_счета} успешно удален."}

def get_clients(db: Session):
    return db.query(Клиент).all()

def get_client_by_id(db: Session, client_id: int):
    return db.query(Клиент).filter(Клиент.id_клиента == client_id).first()

def get_roles(db: Session):
    return db.query(Роль).all()

def get_operations(db: Session):
    return db.query(Операция).all()

def get_street(db: Session):
    return db.query(Улица).all()

def get_account_type(db: Session):
    return db.query(ТипСчета).all()

def get_account_from_type(db: Session):
    return db.query(ВидСчета).options(
        joinedload(ВидСчета.тип),
        joinedload(ВидСчета.процентные_ставки)
    ).all()

def get_interest_rates(db: Session):
    return db.query(ПроцентнаяСтавка).all()

def get_all_branches(db: Session):
    return db.query(Филиал).all()

def get_id_interest_rate(db: Session, id_процентной_ставки: int):
    return db.query(ПроцентнаяСтавка).filter(ПроцентнаяСтавка.id_процентной_ставки == id_процентной_ставки).first()


def update_interest_rate(db: Session, id_процентной_ставки: int, interest_rate: schemas.ПроцентнаяСтавкаBase):
    db_rate = db.query(ПроцентнаяСтавка).filter(ПроцентнаяСтавка.id_процентной_ставки == id_процентной_ставки).first()
    if db_rate is None:
        return None
    db_rate.процентная_ставка = interest_rate.процентная_ставка
    db_rate.дата_изменения = datetime.utcnow()
    db.commit()
    db.refresh(db_rate)
    return db_rate

def is_card_account(account):
    return account.вид.тип.id_типа_счета == 4

def transfer_funds(id_sender_account: int, id_recipient_account: int, amount: int, db):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Сумма перевода должна быть положительной.")

    sender = db.query(Счет).filter(Счет.id_счета == id_sender_account).first()
    recipient = db.query(Счет).filter(Счет.id_счета == id_recipient_account).first()

    if not sender or not recipient:
        raise HTTPException(status_code=404, detail="Один из счетов не найден")

    if not is_card_account(sender) or not is_card_account(recipient):
        raise HTTPException(status_code=403, detail="Перевод возможен только между картами")

    if sender.баланс < amount:
        raise HTTPException(status_code=400, detail="Недостаточно средств на счете отправителя")

    sender.баланс -= amount
    recipient.баланс += amount

    operation = db.query(Операция).filter(Операция.id_операции == 3).first()  # перевод
    if not operation:
        raise HTTPException(status_code=404, detail="Операция 'перевод' не найдена")

    db.add_all([
        БанковскаяОперация(id_счета=sender.id_счета, сумма=-amount,
                                  id_операции=operation.id_операции, дата_операции=datetime.utcnow()),
        БанковскаяОперация(id_счета=recipient.id_счета, сумма=amount,
                                  id_операции=operation.id_операции, дата_операции=datetime.utcnow())
    ])

    db.commit()
    db.refresh(sender)
    db.refresh(recipient)

def cash_withdrawal(id_account: int, amount: int, db):
    account = db.query(Счет).filter(Счет.id_счета == id_account).first()

    if not account:
        raise HTTPException(status_code=404, detail="Счёт не найден")

    if not is_card_account(account):
        raise HTTPException(status_code=403, detail="Снятие возможно только с карты")

    if account.баланс < amount:
        raise HTTPException(status_code=400, detail="Недостаточно средств")

    account.баланс -= amount

    operation = db.query(Операция).filter(Операция.id_операции == 2).first()  # снятие
    if not operation:
        raise HTTPException(status_code=404, detail="Операция 'снятие' не найдена")

    db.add(БанковскаяОперация(
        id_счета=account.id_счета,
        сумма=-amount,
        id_операции=operation.id_операции,
        дата_операции=datetime.utcnow()
    ))

    db.commit()
    db.refresh(account)

def cash_replenishment(id_account: int, amount: int, db):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Сумма должна быть положительной")

    account = db.query(Счет).filter(Счет.id_счета == id_account).first()

    if not account:
        raise HTTPException(status_code=404, detail="Счёт не найден")

    if not is_card_account(account):
        raise HTTPException(status_code=403, detail="Пополнение возможно только карты")

    account.баланс += amount

    operation = db.query(Операция).filter(Операция.id_операции == 1).first()  # пополнение
    if not operation:
        raise HTTPException(status_code=404, detail="Операция 'пополнение' не найдена")

    db.add(БанковскаяОперация(
        id_счета=account.id_счета,
        сумма=amount,
        id_операции=operation.id_операции,
        дата_операции=datetime.utcnow()
    ))

    db.commit()
    db.refresh(account)

class CRUDClient:
    def update_client(self, db: Session, client_id: int, client_update: schemas.КлиентUpdate):
        db_client = db.query(Клиент).filter(Клиент.id_клиента == client_id).first()
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
    impl = LargeBinary
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


# RLS
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_user = get_client_by_id(db, user_id)
    if db_user is None:
        raise credentials_exception

    return TokenData(email=email, id=db_user.id_клиента, role=db_user.id_роли)

def check_operator_access_hours(current_user=Depends(get_current_user)):
    if current_user.role == 3:
        now = datetime.now().time()
        start = time(15, 0)
        end = time(18, 0)
        if not (start <= now <= end):
            raise HTTPException(
                status_code=403,
                detail="Доступ разрешён только с 09:00 до 18:00 для операторов"
            )
    return current_user

def set_rls_context(db: Session, user_id: int):
    db.execute(text(f"SET app.current_client_id = {user_id}"))
