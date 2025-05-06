from .database import Base, engine
from .models import User, Operation

def init_db():
    Base.metadata.create_all(bind=engine)
