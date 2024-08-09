from typing import Any, Dict, List
from bson import ObjectId
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

load_dotenv()

from pymongo import MongoClient

uri = os.getenv("MONGO_URI")
client = MongoClient(uri, tlsAllowInvalidCertificates=True)


try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = FastAPI()
collection = client.Data["Employee"]

class Employee(BaseModel):
    FName: str
    SName: str
    Emp_id: int
    Salary: int
    age: int
    dept: str

@app.post("/insert-data")
def insert_data(employee: Employee):
    try:
        collection.insert_one(employee.model_dump())
        return {"message": "Employee inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert Employee: {e}")


@app.put("/updateEmployee/{Emp_id}")
def update_employee(Emp_id: str, employee: Employee):
    try:
        result = collection.update_one({"_id": ObjectId(Emp_id)}, {"$set": employee.model_dump()})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="employee not found")
        return {"message": "employee updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update employee: {e}")


@app.delete("/delete-employee/{Emp_id}")
def delete_employee(Emp_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(Emp_id)})
        print(result)
        return {"message": "employee deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to update employee: {e}")

