from typing import Union
from typing import List
import mysql.connector
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

# Initialisation de FastAPI
app = FastAPI()

items_db = []

# Création du modèle pour les Items
class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    is_offer: Union[bool, None] = None

# Route par défaut, qui retourne juste un Hello World
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Route qui permet d'afficher un Item
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Route qui permet de créer un Item
@app.post("/items/")
def create_item(item: Item):
    items_db.append(item)
    return item

# Route alternative pour voir les Items
@app.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100):
    return items_db[skip : skip + limit]

# Route qui permet de se connecter à la base de données MySQL venant de l'autre conteneur
@app.get("/mysql")
async def read_root():
    try:
        # Connexion à la base de données à partir des informations de connexion définis dans le docker-compose
        cnx = mysql.connector.connect(user='django', password='secret', host='projet-docker-db-1', database='myAppDB', port=3306, auth_plugin='mysql_native_password')
        cursor = cnx.cursor()
        # Requête basique permettant de vérifier si la connexion marche
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        cursor.close()
        cnx.close()
        # Si la connexion marche retourne un message de success, sinon renvoie une erreur
        return {"status": "success", "version": version[0]}
    except Exception as e:
        return {"status": "error", "message": str(e)}
