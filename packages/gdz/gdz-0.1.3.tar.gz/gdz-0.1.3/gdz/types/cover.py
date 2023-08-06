from pydantic import BaseModel


class Cover(BaseModel):
    title: str
    url: str
