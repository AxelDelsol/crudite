import json
from contextlib import asynccontextmanager

from fastapi import FastAPI

from crudite.tea import Tea
from crudite.tea import router as tea_router
from crudite.tea import store

DB_FILENAME = "teas.json"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Reading data")
    with open(DB_FILENAME, "r") as f:
        teas_json = json.load(f)
        teas = [Tea(**tea) for tea in teas_json["data"]]
        print("Reading data")
        store.set_teas(*teas)

    yield

    with open(DB_FILENAME, "w") as f:
        data = {"data": [tea.model_dump() for tea in store.get_teas()]}
        json.dump(data, f)


app = FastAPI(lifespan=lifespan)
app.include_router(tea_router)
