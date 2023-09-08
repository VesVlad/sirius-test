import sqlalchemy
from sqlalchemy import create_engine
from schema import Base

if __name__ == "__main__":
    engine = create_engine("")
    Base.metadata.create_all(engine)