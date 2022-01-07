from typing import Optional

from fastapi import Body, FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


# you can mix Path, Query and request body parameter declarations freely
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# you can also declare multiple body parameters, e.g. item and user:
@app.put("/items2/{item_id}")
async def update_item2(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# if it is a single value param, FastAPI can suggest it`s a query.
# to instructs it`s not, use Body
@app.put("/items3/{item_id}")
async def update_item3(
    item_id: int, item: Item, user: User, importance: int = Body(...)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# As, by default, singular values are interpreted as query parameters,
# you don't have to explicitly add a Query
@app.put("/items4/{item_id}")
async def update_item4(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# embed: {'item': {...}} instead of {...}
@app.put("/items5/{item_id}")
async def update_item5(item_id: int, item: Item = Body(..., embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


