from fastapi import FastAPI, status

app = FastAPI()


# status_code can be used with any of the path params *get, put, etc.)
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
