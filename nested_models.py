from typing import Dict, List, Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()


# special types
class Image(BaseModel):
    url: HttpUrl
    name: str


# Nested structure: Image as an attribute`s type
# You can also use Pydantic models as subtypes of list, set, etc.
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    images: Optional[List[Image]] = None


# deeply nested models
class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


# Bodies of pure lists
@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


# Have in mind that JSON only supports str as keys.
# But Pydantic has automatic data conversion.
# This means that, even though your API clients can only
# send strings as keys, as long as those strings contain pure integers,
# Pydantic will convert them and validate them.
# And the dict you receive as weights will actually have int keys and float values.
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
