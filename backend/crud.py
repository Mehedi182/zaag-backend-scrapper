from models import ScrapperDataModel
from schemas import ScrapperDataCreate
from sqlalchemy.orm import Session


def create_sample_data(db: Session, sample_data: ScrapperDataCreate):
    db_sample = ScrapperDataModel(**sample_data.model_dump())
    db.add(db_sample)
    db.commit()
    db.refresh(db_sample)
    return db_sample


def get_sample_data(db: Session, sample_id: int):
    return db.query(ScrapperDataModel).filter(ScrapperDataModel.id == sample_id).first()


def get_samples(db: Session):
    return db.query(ScrapperDataModel).all()


def update_sample_data(db: Session, sample_id: int, sample_data: ScrapperDataCreate):
    db_sample = (
        db.query(ScrapperDataModel).filter(ScrapperDataModel.id == sample_id).first()
    )
    if db_sample:
        for key, value in sample_data.dict().items():
            setattr(db_sample, key, value)
        db.commit()
        db.refresh(db_sample)
        return db_sample
    return None


def delete_sample_data(db: Session, sample_id: int):
    db_sample = (
        db.query(ScrapperDataModel).filter(ScrapperDataModel.id == sample_id).first()
    )
    if db_sample:
        db.delete(db_sample)
        db.commit()
        return db_sample
    return None
