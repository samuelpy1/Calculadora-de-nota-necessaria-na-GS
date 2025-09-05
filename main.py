from datetime import datetime
from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base, GradeCalculation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FIAP Grade Calculator", version="1.0.0")


def calcular_gs_minima_para_materia(
    nota_1s: float, nota_cp_2s: float, meta_anual: float
) -> float:
    contrib_primeiro_semestre = nota_1s * 0.4
    nota_necessaria_segundo_semestre = (meta_anual - contrib_primeiro_semestre) / 0.6
    contrib_cp = nota_cp_2s * 0.4
    nota_necessaria_gs = (nota_necessaria_segundo_semestre - contrib_cp) / 0.6
    return round(nota_necessaria_gs, 2)


class CalculationRequest(BaseModel):
    nota_1s: float
    nota_cp_2s: float
    meta_anual: float
    materia: Optional[str] = None


class CalculationResponse(BaseModel):
    id: int
    nota_1s: float
    nota_cp_2s: float
    meta_anual: float
    nota_necessaria_gs: float
    materia: Optional[str]
    created_at: datetime
    message: str


@app.get("/")
def root():
    return {"message": "FIAP Grade Calculator API"}


@app.post("/calculate", response_model=CalculationResponse)
def calculate_grade(request: CalculationRequest, db: Session = Depends(get_db)):
    nota_necessaria_gs = calcular_gs_minima_para_materia(
        request.nota_1s, request.nota_cp_2s, request.meta_anual
    )

    db_calculation = GradeCalculation(
        nota_1s=request.nota_1s,
        nota_cp_2s=request.nota_cp_2s,
        meta_anual=request.meta_anual,
        nota_necessaria_gs=nota_necessaria_gs,
        materia=request.materia,
    )

    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)

    message = f"Para alcançar uma média anual de {request.meta_anual}, você precisa de uma nota mínima de {nota_necessaria_gs} na GS do segundo semestre."

    return CalculationResponse(
        id=db_calculation.id,
        nota_1s=request.nota_1s,
        nota_cp_2s=request.nota_cp_2s,
        meta_anual=request.meta_anual,
        nota_necessaria_gs=nota_necessaria_gs,
        materia=request.materia,
        created_at=db_calculation.created_at,
        message=message,
    )


@app.get("/calculations", response_model=List[CalculationResponse])
def get_calculations(db: Session = Depends(get_db)):
    calculations = db.query(GradeCalculation).all()

    results = []
    for calc in calculations:
        message = f"Para alcançar uma média anual de {calc.meta_anual}, você precisa de uma nota mínima de {calc.nota_necessaria_gs} na GS do segundo semestre."
        results.append(
            CalculationResponse(
                id=calc.id,
                nota_1s=calc.nota_1s,
                nota_cp_2s=calc.nota_cp_2s,
                meta_anual=calc.meta_anual,
                nota_necessaria_gs=calc.nota_necessaria_gs,
                materia=calc.materia,
                created_at=calc.created_at,
                message=message,
            )
        )

    return results


@app.get("/calculations/{calculation_id}", response_model=CalculationResponse)
def get_calculation(calculation_id: int, db: Session = Depends(get_db)):
    calc = (
        db.query(GradeCalculation).filter(GradeCalculation.id == calculation_id).first()
    )

    if not calc:
        raise HTTPException(status_code=404, detail="Calculation not found")

    message = f"Para alcançar uma média anual de {calc.meta_anual}, você precisa de uma nota mínima de {calc.nota_necessaria_gs} na GS do segundo semestre."

    return CalculationResponse(
        id=calc.id,
        nota_1s=calc.nota_1s,
        nota_cp_2s=calc.nota_cp_2s,
        meta_anual=calc.meta_anual,
        nota_necessaria_gs=calc.nota_necessaria_gs,
        materia=calc.materia,
        created_at=calc.created_at,
        message=message,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
