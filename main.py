from fastapi import FastAPI
from App.All_apis import emp_router

def main():
    app = FastAPI()
    app.include_router(emp_router)
    return app

app = main()