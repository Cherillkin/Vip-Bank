from backend.database import Base, engine


print("Удаление всех таблиц...")
Base.metadata.drop_all(bind=engine)

print("Создание новых таблиц...")
Base.metadata.create_all(bind=engine)

print("Готово!")
