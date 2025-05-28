from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LoanBase(BaseModel):
    user_id: int = Field(..., description="ID de l'utilisateur")
    book_id: int = Field(..., description="ID du livre")
    loan_date: Optional[datetime] = Field(None, description="Date d'emprunt")
    due_date: datetime = Field(..., description="Date de retour prévue")
    return_date: Optional[datetime] = Field(None, description="Date de retour effective")

class LoanCreate(BaseModel):
    user_id: int = Field(..., description="ID de l'utilisateur")
    book_id: int = Field(..., description="ID du livre")
    due_date: datetime = Field(..., description="Date de retour prévue")

class LoanUpdate(BaseModel):
    return_date: Optional[datetime] = Field(None, description="Date de retour effective")
    due_date: Optional[datetime] = Field(None, description="Date de retour prévue")

class LoanInDBBase(LoanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Loan(LoanInDBBase):
    pass