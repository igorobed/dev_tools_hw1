from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from typing_extensions import Annotated

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', status_code=200)
def root():
    return ""


@app.post("/post")
def get_post() -> Timestamp:
    return Timestamp()


@app.get("/dog")
def get_dog(kind: Annotated[Optional[DogType], Query(  
    description="Available values: terrier, buldog, dalmatian"
)] = None) -> List[Dog]:
    if kind is None:
        return list(dogs_db.items())
    else:
        return [dog for dog in dogs_db if dog.kind == kind]


@app.post("/dog")
def create_dog(new_dog: Dog) -> Dog:
    new_id = len(dogs_db)
    dogs_db[new_id] = Dog(**new_dog)
    return dogs_db[new_id]


@app.get("/dog/{pk}")
def get_dog_by_pk(pk: int) -> Dog:
    return dogs_db[pk]


@app.patch("/dog/{pk}")
def update_dog(pk: int, dog: Dog) -> Dog:
    dogs_db[pk].name = dog.name
    dogs_db[pk].kind = dog.kind
    return dogs_db[pk]  
