from sqlmodel import SQLModel, create_engine

engine = create_engine("sqlite:///election.db")
def init_db():
    SQLModel.metadata.create_all(engine)