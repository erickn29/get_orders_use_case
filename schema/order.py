from datetime import datetime

from pydantic import BaseModel, Field


class OrderSchema(BaseModel):
    numz: str = Field(max_length=10)
    datez: datetime | None = None
    date: datetime | None = None
    podr: str = Field("", max_length=255)
    podrcd: str = Field("", max_length=64)
    md: str = Field("", max_length=14)
    partn: float = 0
    zak_ustr1: bool = False


class OrderItemSchema(BaseModel):
    code: str = Field(max_length=16)
    name: str | None = None
    qtty: int | None = None
    price: float | None = None
    vendor: str = "Биорич"
    ean13: str = Field("", max_length=13)


class OrderStatusSchema(BaseModel):
    status: str


class OrderSchemaFromFile(BaseModel):
    numz: str = Field(max_length=10)
    date: datetime | None = None
    datez: datetime | None = None
    code: str = Field(max_length=16)
    name: str | None = None
    qtty: int | None = None
    podrcd: str = Field(max_length=64)
    price: float | None = None
    podr: str = Field("", max_length=255)
    md: str = Field("", max_length=14)
    ean13: str = Field("", max_length=13)
    partn: float = 0
    zak_ustr1: bool = False
    vendor: str = "Биорич"
