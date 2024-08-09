from typing import Any, Dict, List
from bson import ObjectId
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import HTTPException, APIRouter
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

emp_router = APIRouter(
    prefix='/emp', tags=["Employee Information"]
)
collection = client.Data["Employee"]

class Employee(BaseModel):
    FName: str
    SName: str
    Emp_id: int
    Salary: int
    age: int
    dept: str

@emp_router.post("/insert-data")
def insert_data(employee: Employee):
    try:
        collection.insert_one(employee.model_dump())
        return {"message": "Employee inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert Employee: {e}")


@emp_router.put("/updateEmployee/{Emp_id}")
def update_employee(Emp_id: str, employee: Employee):
    try:
        result = collection.update_one({"_id": ObjectId(Emp_id)}, {"$set": employee.model_dump()})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="employee not found")
        return {"message": "employee updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update employee: {e}")


@emp_router.delete("/delete-employee/{Emp_id}")
def delete_employee(Emp_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(Emp_id)})
        print(result)
        return {"message": "employee deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"failed to update employee: {e}")


def serialize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively convert MongoDB document to JSON serializable format."""
    for key, value in document.items():
        if isinstance(value, ObjectId):
            document[key] = str(value)
        elif isinstance(value, dict):
            document[key] = serialize_document(value)
        elif isinstance(value, list):
            document[key] = [serialize_document(item) if isinstance(item, dict) else item for item in value]
    return document


@emp_router.get("/fetch-data")
def fetch_data() -> List[Dict[str, Any]]:
    cursor = collection.find()
    data = [serialize_document(doc) for doc in cursor]
    return data
