from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from src.data import load_cars, save_cars, users, Car, User
from starlette.responses import RedirectResponse

app = FastAPI()
templates = Jinja2Templates(directory="src/templates")

@app.get("/cars/search", response_class=HTMLResponse)
def search_cars(request: Request, car_name: Optional[str] = None):
    cars = load_cars()
    if car_name:
        result = [car for car in cars if car_name.lower() in car["name"].lower()]
    else:
        result = []
    return templates.TemplateResponse("cars/search.html", {
        "request": request,
        "cars": result,
        "car_name": car_name or ""
    })


@app.get("/cars/new", response_class=HTMLResponse)
def new_car_form(request: Request):
    return templates.TemplateResponse("cars/new.html", {"request": request})

@app.post("/cars/new")
def create_car(name: str = Form(...), year: str = Form(...)):
    cars = load_cars()
    new_id = max(car["id"] for car in cars) + 1 if cars else 1
    new_car = Car(id=new_id, name=name, year=year)
    cars.append(new_car)
    save_cars(cars)
    return RedirectResponse(url="/cars", status_code=303)

@app.get("/cars", response_model=List[Car])
def get_cars(page: int = 1, limit: int = 10) -> List[Car]:
    cars = load_cars()
    start = (page - 1) * limit
    end = start + limit
    return cars[start:end]


@app.get("/cars/{car_id}", response_model=Car)
def get_car_by_id(car_id: int) -> Car:
    cars = load_cars()
    for car in cars:
        if car["id"] == car_id:
            return car
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/users", response_class=HTMLResponse)
def get_users(request: Request):
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users
    })


@app.get("/users/{user_id}", response_class=HTMLResponse)
def get_user_by_id(request: Request, user_id: int):
    user: Optional[User] = next((u for u in users if u["id"] == user_id), None)
    if user:
        return templates.TemplateResponse("user_detail.html", {
            "request": request,
            "user": user
        })
    return HTMLResponse("Not found", status_code=404)
