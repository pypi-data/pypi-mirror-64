from pydantic import BaseModel


class Price(BaseModel):
    purchase: int
    download: int
