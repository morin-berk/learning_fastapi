from typing import List, Optional

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


# automatically converts some_header to some-header.
# use convert_underscores=False to turn it off
@app.get("/items2/")
async def read_items2(
    strange_header: Optional[str] = Header(None, convert_underscores=False)
):
    return {"strange_header": strange_header}


# duplicate headers -- use List
@app.get("/items3/")
async def read_items3(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}
