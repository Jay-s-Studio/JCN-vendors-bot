"""
Enums for the application
"""
from enum import StrEnum


class BotType(StrEnum):
    """BotType"""
    CUSTOMER = "customer"
    VENDORS = "vendors"
