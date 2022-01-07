from typing import List, Optional

from fastapi import FastAPI, Query

app = FastAPI()


# additional validation with Query
# supports regular expressions
@app.get("/items/")
async def read_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# default values can be different
@app.get("/items2/")
async def read_another_items(q: str = Query("fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# Ellipsis will let FastAPI know that this parameter is required.
@app.get("/items3/")
async def read_third_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


#  To declare a query parameter q that can appear multiple times
#  in the URL, you can write:
@app.get("/items4/")
async def read_fourth_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items
# http://localhost:8000/items/?q=foo&q=bar


# define a default list of values if none are provided:
@app.get("/items5/")
async def read_fifth_items(q: List[str] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items


# add title and description
@app.get("/items6/")
async def read_sixth_items(
    q: Optional[str] = Query(
        None,
        title="Query string",
        description=
        "Query string for the items to search"
        " in the database that have a good match",
        min_length=3,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# use alias if you want a query be not only item_query
@app.get("/items7/")
async def read_seventh_items(q: Optional[str] = Query(None, alias="item-query")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# deprecated=True to show it in the docs
@app.get("/items8/")
async def read_eigth_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


