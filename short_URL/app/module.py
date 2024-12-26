from enum import Enum
from typing import Union, Dict, Optional
from datetime import datetime

from pydantic import BaseModel


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

class PostDB(BaseModel):
    postdb: list[Timestamp]
    max_ind: int

    def create_from_file(self):
        with open('post_db.csv') as f:
            cols = f.readline().replace('\n', '').split(',')
            for row in f:
                row = row.replace('\n', '').split(',')
                args = dict(zip(cols, row))
                self.postdb.append(Timestamp(**args))
                self.max_ind = int(row[0])
        return None
    
    def add_record(self):
        self.max_ind += 1
        ts = int(datetime.now().strftime('%s'))
        self.postdb.append(Timestamp(id=self.max_ind, timestamp=ts))

        csv_record = f'\n{self.max_ind},{ts}'
        with open("post_db.csv", "a") as f:
            f.write(csv_record)
        return None
    
class DogDB(BaseModel):
    db: Dict[int, Dog]
    max_ind: int

    def create_from_file(self):
        with open('dogs_db.csv') as f:
            cols = f.readline().replace('\n', '').split(',')
            for row in f:
                row = row.replace('\n', '').split(',')
                args = dict(zip(cols[1:], row[1:]))
                self.db[int(row[0])] = Dog(**args)
                self.max_ind = int(row[0])
        return None
    
    def put_dog(self, dog:Dog):
        ind = self.max_ind+1
        dog.pk = ind
        self.db[ind] = dog
        self.max_ind = ind

        csv_record = f'\n{dog.pk},{dog.name},{dog.pk},{dog.kind.name}'
        with open("dogs_db.csv", "a") as f:
            f.write(csv_record)
        return dog
    
    def patch_dog(self, pk, dog:Dog):
        dog.pk = pk
        self.db[pk] = dog
        csv_path = 'dogs_db.csv'

        csv_record = f'{dog.pk},{dog.name},{dog.pk},{dog.kind.name}\n'
        with open(csv_path) as f:
            cols = f.readline().replace('\n', '').split(',')
            for row in f:
                if int(row.split(',')[0]) == pk:
                    break
        
        with open(csv_path) as f:
            filedata = f.read()

        filedata = filedata.replace(row, csv_record)

        with open(csv_path, 'w') as f:
            f.write(filedata)
        return dog

if __name__ == "__main__":
    db = DogDB(db={}, max_ind=0)
    db.create_from_file()
    for row in db.db.items():
        print(row)

