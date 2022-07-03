from pydantic import BaseModel

#types
class Item(BaseModel):
    task:str
    