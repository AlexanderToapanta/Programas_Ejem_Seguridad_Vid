"""Modelos Pydantic de entrada."""
from pydantic import BaseModel, Field


class ActualizarNota(BaseModel):
    nota_final: int = Field(..., ge=0, le=100)