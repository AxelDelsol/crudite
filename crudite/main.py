from fastapi import FastAPI

from crudite.tea.router import router as tea_router

app = FastAPI()
app.include_router(tea_router)


@app.get("/")
def root():
    return {"message": "Hello, World"}
