from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Recruits(Base):
    __tablename__ = 'unrecruited_pokemon'

    id = Column(Integer, primary_key=True, index=True)
    pokemon = Column(String)
    region = Column(String)
    area = Column(String)
    method = Column(String)
    dungeon = Column(String)
    notes = Column(String)
    recruited = Column(Boolean, default=False)