"""
Models for currency
"""
from typing import List

from pydantic import BaseModel


class Currency(BaseModel):
    """
    Currency
    """
    name: str
    description: str
    sequence: int


class Currencies(BaseModel):
    """
    Currencies
    """
    currencies: List[Currency]
