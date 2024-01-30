"""
Model for Mixins
"""
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_serializer


class UUIDBaseModel(BaseModel):
    """
    UUID Base Model
    """
    id: Optional[UUID] = Field(default_factory=uuid4)

    @field_serializer("id")
    def serialize_uuid(self, value: UUID, _info) -> str:
        """

        :param value:
        :param _info:
        :return:
        """
        return str(value)
