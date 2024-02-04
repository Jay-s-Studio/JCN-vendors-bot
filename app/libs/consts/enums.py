"""
Enums for the application
"""
from enum import StrEnum


class BotType(StrEnum):
    """BotType"""
    CUSTOMER = "customer"
    VENDORS = "vendors"


class PaymentAccountStatus(StrEnum):
    """PaymentAccountStatus"""
    PREPARING = "preparing"
    OUT_OF_STOCK = "out_of_stock"


class Language(StrEnum):
    """Language"""
    EN_US = "en-us"
    ZH_TW = "zh-tw"
    ZH_CN = "zh-cn"
