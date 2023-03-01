from fastapi import FastAPI, HTTPException
from .models import User,Gender,Role, UserUpdateRequest
from typing import Optional, List
from uuid import UUID, uuid4
import pandas as pd
import json

def car_sales_by_manufacturer_date(date_string:str , Manufacturer:str):
    """
    general function description
    """

    #reads the car sales data 
    car_sales_data = pd.read_csv("data\Car_sales.csv", parse_dates=["Latest_Launch"])

    #generates a filter list 
    filter_bool = ((car_sales_data["Manufacturer"] == Manufacturer) & (car_sales_data["Latest_Launch"] > date_string))
    
    response_data = car_sales_data[filter_bool][["Model" , "Sales_in_thousands" , "Price_in_thousands" , "Latest_Launch"]]

    return response_data




app = FastAPI()

db: List[User] = [
    User(
     id=UUID("6179079b-fc4a-465c-9e08-19690a749a95"),
     first_name="Jamila",
     last_name="Ahmed",
     gender=Gender.female,
     roles=[Role.student]
     ),
     User(
     id=UUID("ad252d19-42ea-482f-a103-2d5fcbf57e70"),
     first_name="Alex",
     last_name="Jones",
     gender=Gender.male,
     roles=[Role.admin, Role.user]
     )
]


@app.get("/")
async def root():
    return {"Hello":"Kili"}

@app.get("/get-cars-by-Manu")
async def get_cars(*, sales_date: Optional[str] = None, car : Optional[str]):
    return car_sales_by_manufacturer_date(sales_date, car)


@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User ):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return 
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code= 404,
        detail= f"user with id: {user_id} does not exists"
    )

