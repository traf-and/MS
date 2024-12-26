from fastapi import FastAPI, HTTPException, status
# import uvicorn
from sqlalchemy import create_engine

from app import module
# import module

app = FastAPI()

# connect/createDB
engine = create_engine('sqlite:////app/data/todo.db', echo=True)
# engine = create_engine('sqlite:///todo.db', echo=True)
conn = engine.connect()
# create table if not exists
module.create_table(engine)

# – POST /items: Создание задачи (title, description?, completed=false).
# – GET /items: Получение списка всех задач.
# – GET /items/{item_id}: Получение задачи по ID.
# – PATCH /items/{item_id}: Обновление задачи по ID.
# – DELETE /items/{item_id}: Удаление задачи


@app.post('/items', summary='Create new task', response_model=module.Task)
async def items_create(task:module.Task)->module.Task:
    task.insert_into_db(conn)
    return task

@app.get('/items', summary='Get all tasks', response_model=module.Tasks)
async def items_get()->module.Tasks:
    tasks = module.Tasks(data = [])
    tasks.get_all_tasks(conn)
    return tasks

@app.get('/items/{item_id}', summary='Get task by id', response_model=module.Task)
async def item_get_id(id:int)->module.Task:

    task = module.Task().get_task_by_id(id, conn)
    return task

@app.patch('/items/{item_id}', summary='Update task by id', response_model=module.Task)
async def item_patch(task:module.Task)->module.Task:
    res = task.update_task_by_id(conn)

    if res == 'ID error':
        raise HTTPException(status_code=404, detail=f"Task with id = {task.id} not exists")
    return task

@app.delete('/items/{item_id}', 
            summary='Delete task by id'
)
async def item_del(id:int):
    res = module.Task().del_task_by_id(id, conn)
    if res == 'ID error':
        raise HTTPException(status_code=404, detail=f"Task with id = {id} not exists")
    return status.HTTP_200_OK

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=10000, reload=True, log_level="debug",
#                 workers=2)