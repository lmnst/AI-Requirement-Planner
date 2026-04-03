from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello! That's my FIRST FastAPI interface"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}! Welcome to the Backend world!"}

