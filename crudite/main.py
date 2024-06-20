from fastapi import FastAPI

from crudite.tea import router as tea_router

app = FastAPI()
app.include_router(tea_router)
