from datetime import timedelta

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, crud, database
from .crud import CRUDClient, ACCESS_TOKEN_EXPIRE_MINUTES
from .utils.backup import backup_database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
        data={"sub": client.email, "id": client.id_клиента, "role": client.role_id},  # payload
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "client_id": client.id_клиента
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

@router.post("/invest_account/", response_model=schemas.ИнвестицииOut)
def create_invest_account(invest_account: schemas.ИнвестицииBase, db: Session= Depends(get_db)):
    return crud.create_invest_account(db, invest_account)

@router.post("/interest_rate/", response_model=schemas.ПроцентнаяСтавкаOut)
def create_interest_rate(interest_rate: schemas.ПроцентнаяСтавкаBase, db: Session = Depends(get_db)):
    return crud.create_interest_rate(db=db, interest_rate=interest_rate)

@router.post("/investment_detail/", response_model=schemas.ДеталиИнвестицийBase)
def create_investment_details(investment_detail: schemas.ДеталиИнвестицийBase, db: Session = Depends(get_db)):
    return crud.create_investment_details(db, investment_detail)

@router.post("/translation")
def transfer_funds(id_sender: int, id_recipient: int, amount: int, db: Session = Depends(get_db)):
    try:
        crud.transfer_funds(id_sender, id_recipient, amount, db)
        return {"message": "Перевод успешно выполнен"}
    except HTTPException as e:
        raise e

@router.post("/withdraw")
def withdraw_cash(id_client: int, amount: int, db: Session = Depends(get_db)):
    try:
        crud.cash_withdrawal(id_client, amount, db)
        return {"message": "Снятие прошло успешно"}
    except HTTPException as e:
        raise e

@router.post("/replenishment")
def replenishment_cash(id_client: int, amount: int, db: Session = Depends(get_db)):
    try:
        crud.cash_replenishment(id_client, amount, db)
        return {"message": "Пополнение прошло успешно"}
    except HTTPException as e:
        raise e

@router.post("/yield/calculate/{briefcase_id}", response_model=schemas.ДоходностьИнвестицийOut)
def calculate_yield(briefcase_id: int, db: Session = Depends(get_db)):
    return crud.calculate_and_create_yield(db, briefcase_id)

@router.put("/interest_rate/{id_interest_rate}/update_at", response_model=schemas.ПроцентнаяСтавкаOut)
def update_interest_rate_at(id_interest_rate: int, db: Session = Depends(get_db)):
    db_rate = crud.update_дата_изменения(db=db, id_процентной_ставки=id_interest_rate)
    if db_rate is None:
        raise HTTPException(status_code=404, detail="Процентная ставка не найдена")
    return db_rate

@router.delete("/account_types/{account_type_id}", response_model=dict)
def delete_account_from_type(id_account_from_type: int, db: Session = Depends(get_db)):
    return crud.delete_account_type_by_id(db=db, id_вида_счета=id_account_from_type)

@router.get("/clients/{client_id}", response_model=schemas.КлиентOut)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_id(db, client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Клиент не найден")
    return db_client

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

@router.get("/invest_account/{id_briefcase}", response_model=schemas.ИнвестицииOut)
def get_invest_account_by_id(id_invest_account: int, db: Session = Depends(get_db)):
    return crud.get_invest_account_by_id(db, id_invest_account)

@router.get("/types_invest", response_model=List[schemas.ТипИнвестицийOut])
def get_all_types_invest(db: Session = Depends(get_db)):
    return crud.get_all_type_invest(db)

@router.get("/investment-details/by-briefcase/{briefcase_id}", response_model=List[schemas.ДеталиИнвестицийOut])
def read_investment_details_by_briefcase(briefcase_id: int, db: Session = Depends(get_db)):
    return crud.get_investment_details_by_briefcase_id(db, briefcase_id)

@router.get("/yield/{briefcase_id}", response_model=schemas.ДоходностьИнвестицийOut)
def read_yield_by_briefcase_id(briefcase_id: int, db: Session = Depends(get_db)):
    return crud.get_yield_by_briefcase_id(db, briefcase_id)



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