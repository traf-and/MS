from typing import List
from fastapi import FastAPI
import uvicorn

import module

app = FastAPI()

dogs_db = module.DogDB(db={}, max_ind=0)
dogs_db.create_from_file()

post_db = module.PostDB(postdb=[], max_ind=0)
post_db.create_from_file()


@app.get('/', response_model=str)
async def root()->str:
    return 'OK'

@app.post('/post', summary='Get Post', response_model=module.Timestamp)
async def get_post()->module.Timestamp:
    return post_db.postdb[-1]

@app.get('/dog', summary='Get Dogs', response_model=List[module.Dog])
async def get_dog(
    kind:module.DogType
    )->List[module.Dog]:
    dog_list = []
    
    for i in dogs_db.db.values():
        if kind == i.kind:
            dog_list.append(i)
    return dog_list

@app.post('/dog', summary='Create Dog', response_model=module.Dog)
async def post_Dog(dog:module.Dog)->module.Dog:
    dog = dogs_db.put_dog(dog)
    post_db.add_record()
    return dog

@app.get('/dog/{pk}', summary='Get Dog By Pk', response_model=module.Dog)
async def get_dog(
    pk:int
    )->module.Dog:
    return dogs_db.db[pk]

@app.patch('/dog/{pk}', summary='Update Dog', response_model=module.Dog)
async def get_dog(
    pk:int,
    dog:module.Dog
    )->module.Dog:
    dog = dogs_db.patch_dog(pk, dog)
    post_db.add_record()
    return dog

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=10000, reload=True, log_level="debug",
                workers=2)