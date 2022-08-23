from enum import Enum
from typing import List, Union
from fastapi import FastAPI, Path, Query, Body
import uvicorn
from pydantic import BaseModel

# List of models
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class ModelName(str, Enum):
    alpha = "alpha"
    beta = "beta"
    gamma = "gamma"


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alpha:
        return {"model_name": model_name, "message": "Alpha is called"}

    if model_name.value == ModelName.beta:
        return {"model_name": model_name, "message": "Beta is called"}

    if model_name.value == ModelName.gamma:
        return {"model_name": model_name, "message": "Gamma is called"}

    return {"model_name": model_name, "message": "Test model message"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# users
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# items
@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None,
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


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price * item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    q: Union[str, None] = Query(default=None, alias="item-query"),
    size: float = Query(gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

