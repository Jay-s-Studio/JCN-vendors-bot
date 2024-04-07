"""
Contains all the messages used in the telegram bot.
"""
from pydantic import BaseModel, Field
from collections import defaultdict
from typing import Dict, Optional

from telegram.constants import ParseMode

from app.libs.consts.enums import Language


class Message(BaseModel):
    text: str
    parse_mode: Optional[ParseMode] = Field(default=None)


class MessagesBase:
    """MessagesBase"""
    message: Dict[Language, str] = defaultdict(Dict[Language, str])
    parse_mode: Optional[ParseMode] = None

    def __getitem__(self, language: Language):
        """
        get item
        :param language:
        :return:
        """
        return self.message[language]

    @classmethod
    def format(cls, language: Language = Language.EN_US, *args, **kwargs) -> Message:
        """
        format
        :param language:
        :param args:
        :param kwargs:
        :return:
        """
        return Message(
            text=cls.message.get(language, Language.EN_US).format(*args, **kwargs),
            parse_mode=cls.parse_mode
        )


class ExchangeRateMessage(MessagesBase):
    """ExchangeRateMessage"""
    message = {
        Language.EN_US: "Please provide the latest exchange rate information, "
                        "click \"Provide\" and reply in <strong>1 hour</strong>."
    }
    parse_mode = ParseMode.HTML


class PaymentAccountMessage(MessagesBase):
    """
    PaymentAccountMessage
    """
    message = {
        Language.EN_US: "Please provide the payment account information for `{total_amount}` `{payment_currency}` to exchange `{exchange_currency}`."
    }
    parse_mode = ParseMode.MARKDOWN


class PaymentAccountStatusMessage(MessagesBase):
    """
    PaymentAccountStatusMessage
    """
    message = {
        Language.EN_US: "Please select your current payment account status\."
    }
    parse_mode = ParseMode.MARKDOWN_V2


class HurryPaymentAccountMessage(MessagesBase):
    """
    HurryPaymentAccountMessage
    """
    message = {
        Language.EN_US: "Please provide payment account information for `{total_amount}` `{payment_currency}` "
                        "as soon as possible to redeem `{exchange_currency}`."
    }
    parse_mode = ParseMode.MARKDOWN


class ConfirmPayMessage(MessagesBase):
    """
    ConfirmPayMessage
    """
    message = {
        Language.EN_US: "Customer has paid, please check the payment account and confirm the payment\."
    }
    parse_mode = ParseMode.MARKDOWN_V2
