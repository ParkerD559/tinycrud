import uvicorn
from tinydb import TinyDB, Query
from fastapi import FastAPI
from pydantic import BaseModel

class Version(BaseModel):
    version: int


class TinyCRUD(object):
    def __init__(self):
        self.api = FastAPI()
        self.db = TinyDB("db.json")
        self.query = Query()

    def resource(self, name, value=None):
        if value:
            self.db.upsert({ name: value }, self.query[name])
        @self.api.get(f"/{name}")
        def get():
            return self.db.get(self.query[name])
        @self.api.put(f"/{name}")
        def put(new_value: Version):
            self.db.upsert(new_value, self.query[name])

    def run(self):
        uvicorn.run(self.api)
