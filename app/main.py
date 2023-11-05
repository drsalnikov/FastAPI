from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType
    def __str__(self):
        return f"{self.kind.name} {self.name}"

class Timestamp(BaseModel):
    id: int
    timestamp: int
    def __str__(self):
        return f"{self.id} {self.timestamp}"

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


def page(content:str):
    data = ""
    with open("wwwroot/index.html", 'r') as f: 
        data = f.read().replace("{data}", content)
    return HTMLResponse(data)


def create_list_by_dict(list:dict):
    content = "<ul>"
    for el in list:
        content += f"<li>{el} {list[el]}</li>"
    content += "</ul>"
    print(content)
    return content


def create_list(list:list):
    content = "<ul>"
    for el in list:
        content += f"<li>{el}</li>"
    content += "</ul>"
    return content


@app.get('/')
async def root():
    content = "<h1>Бобро пожаловать!</h1>"
    content += "<ul>"
    content += "<li><a href='dog'>Посмотреть всех собак</a></li>"
    content += "<li><a href='dog/type'>Фильтрация по типу</a></li>"
    content += "<li><a href='redoc'>Документация</a></li>"
    content += "<li><a href='docs'>Альтернативная документация</a></li>"
    content += "</ul>"
    return page(content)



@app.post('/post')
async def post(ts:Timestamp):
    ids = [item.id for item in post_db]
    if not ts.id in ids:
        post_db.append(ts)

    return str(post_db)


@app.get('/dog')
async def GetDogs():
    content = create_list_by_dict(dogs_db)
    return page(f"<h1>Dogs</h1> {content}")


@app.post('/dog')
async def CreateDog(dog:Dog):
    last_id = max(dogs_db.keys()) + 1
    dogs_db[last_id] = dog
    content = create_list_by_dict(dogs_db)
    return page(f"<h1>Dogs</h1> {content}")


@app.patch('/dog/{dog_id}')
async def UpdateDog(dog:Dog, dog_id:int):
    dogs_db[dog_id] = dog
    content = create_list_by_dict(dogs_db)
    return page(f"<h1>Dogs</h1> {content}")


@app.get('/dog/type/{dog_type}')
async def GetDog(dog_type:DogType):
    dogs = [el for el in dogs_db.values() if el.kind == dog_type]
    content = create_list(dogs)
    return page(content)


@app.get('/dog/type')
async def DogTypes():
    dogs = [el.value for el in DogType]
    content = "<ul>"
    for dogtype in dogs:
        content += f"<li><a href='/dog/type/{dogtype}'>{dogtype}</a></li>"
    content += "</ul>"
    return page(content)


@app.get('/dog/{dog_id}')
async def GetDog(dog_id:int):
    return page(str(dogs_db.get(dog_id, 0)))

