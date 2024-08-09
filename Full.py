# import os
# from fastapi import FastAPI, HTTPException
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# from bson import ObjectId
# from pydantic import BaseModel
# import jwt
# from typing import List, Dict, Any
# from dotenv import load_dotenv

# load_dotenv()

# uri = os.getenv("MONGO_URI")

# client = MongoClient(uri, server_api=ServerApi('1'))

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print("Failed to connect to MongoDB:", e)

# app = FastAPI()


# @app.get("/check")
# def check():
#     encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
#     jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
#     return f"Apis Working + {encoded_jwt}"


# def serialize_document(document: Dict[str, Any]) -> Dict[str, Any]:
#     """Recursively convert MongoDB document to JSON serializable format."""
#     for key, value in document.items():
#         if isinstance(value, ObjectId):
#             document[key] = str(value)
#         elif isinstance(value, dict):
#             document[key] = serialize_document(value)
#         elif isinstance(value, list):
#             document[key] = [serialize_document(item) if isinstance(item, dict) else item for item in value]
#     return document


# collection = client.dashboard["products"]


# @app.get("/fetch-data")
# def fetch_data() -> List[Dict[str, Any]]:
#     cursor = collection.find()
#     data = [serialize_document(doc) for doc in cursor]
#     return data


# class Product(BaseModel):
#     title: str
#     desc: str
#     price: int
#     stock: int
#     img: str
#     color: str
#     size: str
#     createdAt: str


# @app.post("/insert-data")
# def insert_data(product: Product):
#     try:
#         collection.insert_one(product.model_dump())
#         return {"message": "Product inserted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to insert product: {e}")


# @app.put("/update-product/{product_id}")
# def update_product(product_id: str, product: Product):
#     try:
#         result = collection.update_one({"_id": ObjectId(product_id)}, {"$set": product.model_dump()})
#         if result.matched_count == 0:
#             raise HTTPException(status_code=404, detail="Product not found")
#         return {"message": "Product updated successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to update product: {e}")


# @app.delete("/delete-product/{product_id}")
# def delete_product(product_id: str):
#     try:
#         result = collection.delete_one({"_id": ObjectId(product_id)})
#         print(result)
#         # if result.deleted_count < 0:
#         #     raise HTTPException(status_code=404, detail="Product not found")
#         return {"message": "Product deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"failed to update product: {e}")


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

