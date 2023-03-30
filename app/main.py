from typing import Union
from typing import List
import mysql.connector
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

items_db = []

class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
def create_item(item: Item):
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100):
    return items_db[skip : skip + limit]

@app.get("/mysql")
async def read_root():
    try:
        cnx = mysql.connector.connect(user='django', password='secret', host='projetdocker-db-1', database='myAppDB', port=3306, auth_plugin='mysql_native_password')
        cursor = cnx.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        cursor.close()
        cnx.close()
        return {"status": "success", "version": version[0]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
