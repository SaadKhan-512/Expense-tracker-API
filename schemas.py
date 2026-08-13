from pydantic import  BaseModel

class expenses_schema(BaseModel):
    name: str
    category: str
    price: float

class date_schema(BaseModel):
    start: str
    end: str