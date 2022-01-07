from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# supports Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/")
def read_root():
    return {"Hello": "World"}


# order matters
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# supports query parameters
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_price": item.price, "item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# the URL for that file would be something like: /files/home/johndoe/myfile.txt

# the name of the parameter is file_path,
# and the last part, :path, tells
# it that the parameter should match any path
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# bool can be one of the following: on/off, yes/no, true/false
@app.get("/things/{thing_id}")
async def read_thing(thing_id: str, q: Optional[str] = None, short: bool = False):
    thing = {"thing_id": thing_id}
    if q:
        thing.update({"q": q})
    if not short:
        thing.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return thing


# You can declare multiple path parameters and query parameters at the same time
# And you don't have to declare them in any specific order
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# required query param
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item


# some parameters as required,
# some as having a default value,
# and some entirely optional:
@app.get("/another_items/{item_id}")
async def read_another_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# declare path parameters and request body at the same time
@app.put("/items/{item_id}")
async def create_another_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}


# You can also declare body, path and query parameters, all at the same time.
# If the parameter is declared to be of the type of a Pydantic model,
# it will be interpreted as a request body
@app.put("/items/{item_id}")
async def create_third_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result


