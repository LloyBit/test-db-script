from script.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

class Database():
    def __init__(self):
        self.engine = create_engine(settings.database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    # Контекстный менеджер для работы с сессией и ее авто-закрытия 
    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
            
    def close(self):
        self.engine.dispose()
        
database = Database()