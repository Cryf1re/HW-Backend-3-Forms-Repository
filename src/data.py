import json
from typing import List, TypedDict


class Car(TypedDict):
    id: int
    name: str
    year: str


class User(TypedDict):
    id: int
    email: str
    first_name: str
    last_name: str
    username: str


users: List[User] = [
    {
        "id": 1,
        "email": "test1@test.com",
        "first_name": "Aibek",
        "last_name": "Bekturov",
        "username": "deadly_knight95",
    },
    {
        "id": 2,
        "email": "test2@test.com",
        "first_name": "Aliya",
        "last_name": "Nurkenova",
        "username": "sunshine_aliya",
    },
    {
        "id": 3,
        "email": "test3@test.com",
        "first_name": "Daniyar",
        "last_name": "Zhaksylykov",
        "username": "danikz",
    },
]


def load_cars() -> List[Car]:
    with open("src/data/cars.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_cars(cars: List[Car]):
    with open("src/data/cars.json", "w", encoding="utf-8") as f:
        json.dump(cars, f, indent=4)
