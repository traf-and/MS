from enum import Enum
from typing import List, Optional
from datetime import date
import random
import string

from sqlalchemy import Engine, Table, MetaData, Column, String, Integer, Connection, inspect, insert, text, select
from pydantic import BaseModel

metadata_obj = MetaData() 
urls = Table(
    'urls',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('short_url', String),
    Column('url', String)
)

def create_table(engine:Engine):
    tables = inspect(engine).get_table_names()
    if 'urls' not in tables:
        metadata_obj.create_all(engine)
    return None

class ShortURL(BaseModel):
    short_url:Optional[str] = None

    def get_short_url_by_id(self, conn:Connection, url_id:int):
        stmt = select(urls).filter(urls.c.id == url_id)
        response = conn.execute(stmt)
        response = response.fetchall()
        self.short_url = response[0][1] if response else None
        return self
    
    def get_full_url(self, conn:Connection):
        stmt = select(urls).filter(urls.c.short_url == self.short_url)
        response = conn.execute(stmt)
        response = response.fetchall()
        full_url = response[0][-1] if response else None
        url = URL(url=full_url)
        return url

class URL(BaseModel):
    url:Optional[str] = None

    def generate_short_id(self, conn:Connection, length:int = 6):
        characters = string.ascii_letters + string.digits
        short_url = ''.join(random.choice(characters) for _ in range(length))
        stmt = select(urls).filter(urls.c.short_url == short_url)
        response = conn.execute(stmt)
        response = response.fetchall()
        return response, short_url

    def url_in_db(self, conn:Connection)->Optional[int]:
        stmt = select(urls).filter(urls.c.url == self.url)
        response = conn.execute(stmt)
        response = response.fetchall()
        url_id = response[0][0] if response else None
        
        return url_id

    def create_short_id(self, conn:Connection, length:int = 6)->None:
        
        url_id = self.url_in_db(conn)

        if isinstance(url_id, int):
            short_url = ShortURL()
            short_url.get_short_url_by_id(conn, url_id)
            return short_url


        response, short_url = self.generate_short_id(conn)
        while response:
            response, short_url = self.generate_short_id(conn)

        short_url = ShortURL(short_url=short_url)
        response = conn.execute(text('SELECT max(id) FROM urls'))
        response = [row[0] for row in response][0]
        max_ind = 0 if response is None else response+1
        
        row = URLInfo(url=self.url, 
                      short_url=short_url.short_url, 
                      id=max_ind)
        stmt = insert(urls).values(row.model_dump())
        conn.execute(stmt)
        conn.commit()
        return short_url

class URLInfo(BaseModel):
    id:Optional[int] = None
    url:Optional[str] = None
    short_url:Optional[str] = None

    def info_by_short(self, short_url:ShortURL, conn:Connection)->None:
        stmt = select(urls).filter(urls.c.short_url == short_url.short_url)
        response = conn.execute(stmt)
        urlinfo = URLInfo(**response.mappings().all()[0]) 

        return urlinfo

if __name__ == "__main__":
    print('OK')