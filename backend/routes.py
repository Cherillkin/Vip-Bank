from datetime import timedelta, date

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from . import schemas, crud, database, models
from .crud import CRUDClient, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_user, check_operator_access_hours
from .schemas import TokenData
from .utils.backup import backup_database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/admin/create-user", response_model=schemas.КлиентOut)
def admin_create_user(
    client: schemas.КлиентCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user.role != 2:
        raise HTTPException(status_code=403, detail="Нет доступа")
    if client.id_роли not in [2, 3]:
        raise HTTPException(status_code=400, detail="Можно создавать только админов и операторов")
    return crud.create_admin_or_operator(db, client)

@router.post("/clients/", response_model=schemas.КлиентOut)
def create_client_route(client: schemas.КлиентCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, client)

@router.put("/clients/{client_id}/update_at", response_model=schemas.КлиентUpdate)
def update_client_route(client_id: int, client_update: schemas.КлиентUpdate, db: Session = Depends(get_db)):
    crud_client = CRUDClient()
    updated_client = crud_client.update_client(db=db, client_id=client_id, client_update=client_update)
    return updated_client


@router.post("/login/")
def login(credentials: schemas.КлиентLogin, db: Session = Depends(get_db)):
    client = crud.authenticate_client(db, credentials.email, credentials.пароль)
    if not client:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": client.email, "id": client.id_клиента, "role": client.id_роли},  # payload
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "client_id": client.id_клиента,
        "role_id": client.id_роли
    }

@router.post("/roles/", response_model=schemas.РольOut)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return crud.create_role(db, role)

@router.post("/street/", response_model=schemas.УлицаOut)
def create_street(street: schemas.УлицаOut, db: Session = Depends(get_db)):
    return crud.create_street(db, street)

@router.post("/branch/", response_model=schemas.ФилиалOut)
def create_branch(branch: schemas.ФилиалOut, db: Session = Depends(get_db)):
    return crud.create_branch(db, branch)

@router.post("/account_from_type/", response_model=schemas.ВидСчетаOut)
def create_account_from_type(account_type: schemas.ВидСчетаBase, db: Session = Depends(get_db)):
    return crud.create_account_from_type(db, account_type)

@router.post("/account/", response_model=schemas.СчетOut)
def create_account(account: schemas.СчетBase, db: Session = Depends(get_db)):
    return crud.create_account(db, account)

@router.post("/interest_rate/", response_model=schemas.ПроцентнаяСтавкаOut)
def create_interest_rate(interest_rate: schemas.ПроцентнаяСтавкаBase, db: Session = Depends(get_db)):
    return crud.create_interest_rate(db=db, interest_rate=interest_rate)

@router.post("/translation")
def transfer_funds(id_sender_account: int, id_recipient_account: int, amount: int, db: Session = Depends(get_db)):
    try:
        crud.transfer_funds(id_sender_account, id_recipient_account, amount, db)
        return {"message": "Перевод успешно выполнен"}
    except HTTPException as e:
        raise e

@router.post("/withdraw")
def withdraw_cash(id_account: int, amount: int, db: Session = Depends(get_db)):
    try:
        crud.cash_withdrawal(id_account, amount, db)
        return {"message": "Снятие прошло успешно"}
    except HTTPException as e:
        raise e

@router.post("/replenishment")
def replenishment_cash(id_account: int, amount: int, db: Session = Depends(get_db)):
    try:
        crud.cash_replenishment(id_account, amount, db)
        return {"message": "Пополнение прошло успешно"}
    except HTTPException as e:
        raise e

# @router.post("/yield/calculate/{briefcase_id}", response_model=schemas.ДоходностьИнвестицийOut)
# def calculate_yield(briefcase_id: int, db: Session = Depends(get_db)):
#     return crud.calculate_and_create_yield(db, briefcase_id)

@router.put("/interest_rate/{id_interest_rate}", response_model=schemas.ПроцентнаяСтавкаOut)
def update_interest_rate(id_interest_rate: int, updated_rate: schemas.ПроцентнаяСтавкаBase, db: Session = Depends(get_db)):
    db_rate = crud.update_interest_rate(db=db, id_процентной_ставки=id_interest_rate, interest_rate=updated_rate)
    if db_rate is None:
        raise HTTPException(status_code=404, detail="Процентная ставка не найдена")
    return db_rate

@router.delete("/account_types/{account_type_id}", response_model=dict)
def delete_account_from_type(id_account_from_type: int, db: Session = Depends(get_db)):
    return crud.delete_account_type_by_id(db=db, id_вида_счета=id_account_from_type)

@router.delete("/account/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def close_account(account_id: int, client_id: int, db: Session = Depends(get_db)):
    account = db.query(models.Счет).filter(
        models.Счет.id_счета == account_id,
        models.Счет.id_клиента == client_id
    ).first()

    if not account:
        raise HTTPException(status_code=404, detail="Счет не найден")

    if account.баланс < 0:
        raise HTTPException(status_code=400, detail="Баланс отрицательный, счет нельзя закрыть")
    elif account.баланс > 0:
        card_account = db.query(models.Счет).join(models.ВидСчета).filter(
            models.Счет.id_клиента == client_id,
            models.ВидСчета.id_типа_счета == 4
        ).first()

        if not card_account:
            raise HTTPException(status_code=400, detail="Пластиковая карта клиента не найдена")

        card_account.баланс += account.баланс
        account.баланс = 0

    db.delete(account)
    db.commit()

@router.get("/clients/{client_id}", response_model=schemas.КлиентOut)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(crud.get_current_user)
):
    if current_user.role != 2:
        crud.set_rls_context(db, current_user.id)

    db_client = crud.get_client_by_id(db, client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return db_client

@router.get("/clients", response_model=List[schemas.КлиентOut])
def get_clients(
    db: Session = Depends(get_db),
    current_user=Depends(check_operator_access_hours)
):
    if current_user.role not in [2, 3]:
        raise HTTPException(status_code=403, detail="Нет доступа")
    return db.query(models.Клиент).all()


@router.get("/roles", response_model=list[schemas.РольOut])
def get_all_roles(db: Session = Depends(get_db)):
    roles = crud.get_roles(db)
    return roles

@router.get("/operations", response_model=list[schemas.ОперацияOut])
def get_all_operations(db: Session = Depends(get_db)):
    operations = crud.get_operations(db)
    return operations

@router.get("/streets", response_model=list[schemas.УлицаOut])
def get_all_streets(db: Session = Depends(get_db)):
    streets = crud.get_street(db)
    return streets

@router.get("/account_types", response_model=list[schemas.ТипСчетаOut])
def get_all_account_types(db: Session = Depends(get_db)):
    account_types = crud.get_account_type(db)
    return account_types

@router.get("/account_from_types", response_model=list[schemas.ВидСчетаOut])
def get_all_account_from_types(db: Session = Depends(get_db)):
    account_from_types_types = crud.get_account_from_type(db)
    return account_from_types_types

@router.get("/interest_rates", response_model=list[schemas.ПроцентнаяСтавкаOut])
def get_interest_rates(db: Session = Depends(get_db)):
    interest_rates = crud.get_interest_rates(db)
    return interest_rates

@router.get("/branches", response_model=list[schemas.ФилиалOut])
def get_all_branches(db: Session = Depends(get_db)):
    branches = crud.get_all_branches(db)
    return branches

@router.get("/interest_rate/{id_interest_rate}", response_model=schemas.ПроцентнаяСтавкаOut)
def get_interest_rate_by_id(id_interest_rate: int, db: Session = Depends(get_db)):
    return crud.get_id_interest_rate(db=db, id_процентной_ставки=id_interest_rate)

@router.get("/account/{id_account}", response_model=schemas.СчетOut)
def get_account_by_id(id_account: int, db: Session = Depends(get_db)):
    return crud.get_account_by_id(db, id_account)

@router.get("/accounts/client/{client_id}", response_model=List[schemas.СчетOut])
def get_accounts_by_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    if current_user.role != 2 and current_user.id != client_id:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    accounts = crud.get_accounts_by_client_id(db, client_id)
    if not accounts:
        raise HTTPException(status_code=404, detail="Счета не найдены")
    return accounts

@router.get("/accounts/{account_id}/card-operations/", response_model=List[schemas.БанковскаяОперацияOut])
def get_card_operations_by_account(
    account_id: int,
    start_date: date = Query(..., description="Дата начала периода"),
    end_date: date = Query(..., description="Дата конца периода"),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    account = db.query(models.Счет).filter(models.Счет.id_счета == account_id).first()

    if account.id_клиента != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ к счёту запрещён.")

    operations = crud.get_card_operations_by_account(db, account_id, start_date, end_date)
    return operations

@router.get("/operations/by-account/{account_id}", response_model=List[schemas.БанковскаяОперацияOut])
def get_all_operations_by_account(
    account_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user)
):
    account = db.query(models.Счет).filter(models.Счет.id_счета == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Счёт не найден")

    if account.id_клиента != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ к счёту запрещён")

    operations = crud.get_all_operations_by_account(db, account_id)
    return operations

@router.get("/operations/history", response_model=List[schemas.БанковскаяОперацияOut])
def get_all_operations(
    db: Session = Depends(get_db),
    current_user=Depends(check_operator_access_hours)
):
    if current_user.role not in [2, 3]:
        raise HTTPException(status_code=403, detail="Нет доступа")
    return db.query(models.БанковскаяОперация).all()


@router.get("/types_invest", response_model=List[schemas.ТипИнвестицийOut])
def get_all_types_invest(db: Session = Depends(get_db)):
    return crud.get_all_type_invest(db)


# Для бэкапа БД
@router.post("/backup")
def create_backup():
    result = backup_database(
        db_name="vip_bank",
        user="postgres",
        output_dir="backups",
        host="localhost"
    )
    return result