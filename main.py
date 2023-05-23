from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Created FastAPI project. Gotta implement DB now."}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
