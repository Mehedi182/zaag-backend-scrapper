from database import Base
from sqlalchemy import Column, Float, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class ScrapperDataModel(Base):
    __tablename__ = "scrapper_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # _class = Column(String, nullable=True)
    tax_id = Column(String, nullable=True)
    gtdb_id = Column(String, nullable=True)
    domain = Column(String, nullable=True)
    abundance_score = Column(Float, nullable=True)
    relative_abundance = Column(Float, nullable=True)
    unique_matches = Column(Float, nullable=True)
    total_matches = Column(Float, nullable=True)
    unique_matches_frequency = Column(Float, nullable=True)
    reads_frequency = Column(Integer, nullable=True)
    normalized_reads_frequency = Column(Integer, nullable=True)
    go_id = Column(String, nullable=True)
    go_category = Column(String, nullable=True)
    go_description = Column(String, nullable=True)
    copies_per_million = Column(Float, nullable=True)  # cpm
    enzyme_id = Column(String, nullable=True)
    pfam_id = Column(String, nullable=True)
    cazy_id = Column(String, nullable=True)
