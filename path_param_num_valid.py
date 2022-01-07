from typing import Optional

from fastapi import FastAPI, Path, Query

app = FastAPI()


# validation of path params through Path
@app.get("/items/{item_id}")
async def read_items(
    # if use None not ... a param will still be required
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Order the parameters as you need. FastAPI doesnt care about order


# pass * as the first parameter of the func, so the following will be kwargs
@app.get("/items2/{item_id}")
async def read_second_items(
    *, item_id: int = Path(..., title="The ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# gt: greater than
# le: less than or equal
# ge  "greater than or equal"
@app.get("/items3/{item_id}")
async def read_third_items(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: str,
    size: float = Query(..., gt=0, lt=10.5)
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
