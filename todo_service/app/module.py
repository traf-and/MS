from enum import Enum
from typing import List, Optional
from datetime import date

from sqlalchemy import Engine, Table, MetaData, Column, String, Integer, Date, Connection, inspect, insert, text
from pydantic import BaseModel


metadata_obj = MetaData() 
tasks = Table(
    'tasks',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('title', String),
    Column('description', String),
    Column('completed', Integer),
    Column('status', String),
    Column('plane_date', Date),
    Column('end_date', Date)
)

def create_table(engine:Engine):
    tables = inspect(engine).get_table_names()
    if 'tasks' not in tables:
        metadata_obj.create_all(engine)
    return None

class Status(str, Enum):
    new = "new"
    in_work = "in_work"
    test = "test"
    complete = "complete"

# title, description?, completed=false
class Task(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    plane_date: Optional[date] = None
    end_date: Optional[date] = None

    def insert_into_db(self, conn: Connection)->None:
        response = conn.execute(text('SELECT max(id) FROM tasks'))
        response = [row[0] for row in response][0]
        max_ind = 0 if response is None else response+1
        self.id = max_ind
        stmt = insert(tasks).values(self.model_dump())
        conn.execute(stmt)
        conn.commit()
        return None
    
    def get_task_by_id(self, id:int, conn: Connection):
        query = f"""SELECT id, title, description, status, plane_date, end_date
        FROM tasks
        where id={id};
        """
        response = conn.execute(text(query))
        response = response.mappings().all()
        if len(response)==0:
            return self
        # print(response.mappings().all()[0])
        task = Task(**response[0])
        return task
    
    def update_task_by_id(self, conn: Connection) -> str:
        query = f"""UPDATE tasks
        set title = '{self.title}', 
            description = '{self.description}', 
            status = '{self.status.value}', 
            plane_date = date('{self.plane_date}'), 
            end_date = date('{self.end_date}')
        where id={self.id};
        """
        respone = conn.execute(text(query))
        
        if respone.rowcount==0:
            conn.rollback()
            return 'ID error'
        
        conn.commit()
        return 'Ok'
    
    def del_task_by_id(self, id:int, conn:Connection) -> str:
        query = f"""DELETE from tasks
        where id={id};
        """
        respone = conn.execute(text(query))
        
        if respone.rowcount==0:
            conn.rollback()
            return 'ID error'
        
        conn.commit()
        return 'Ok'


class Tasks(BaseModel):
    data: List[Task]

    def get_all_tasks(self, conn: Connection)->List[Task]:
        query = """SELECT id, title, description, status, plane_date, end_date
        FROM tasks 
        ORDER BY 1
        """
        response = conn.execute(text(query))
        self.data = [Task(**i) for i in response.mappings().all()]
        return None

if __name__ == "__main__":
    print('OK')