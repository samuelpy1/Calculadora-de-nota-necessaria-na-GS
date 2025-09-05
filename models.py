from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from database import Base

class GradeCalculation(Base):
    __tablename__ = "grade_calculations"
    
    id = Column(Integer, primary_key=True, index=True)
    nota_1s = Column(Float, nullable=False)
    nota_cp_2s = Column(Float, nullable=False)
    meta_anual = Column(Float, nullable=False)
    nota_necessaria_gs = Column(Float, nullable=False)
    materia = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())