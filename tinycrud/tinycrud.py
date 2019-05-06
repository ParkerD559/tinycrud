import uvicorn
from tinydb import TinyDB, Query
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class TinyCRUD(object):
    def __init__(self):
        self.api = FastAPI()
        self.db = TinyDB("db.json")

    def collection(self, name: str, schema: BaseModel):
        table = self.db.table(name)
        
        @self.api.post(f"/{name}", status_code=201)
        def create(body: schema):
            return {
                "id": table.insert(body.dict())
            }

        @self.api.get(f"/{name}/{{id}}")
        def read(id: int):
            user = table.get(doc_id=id)
            if not user:
                raise HTTPException(status_code=404)
            return user

        @self.api.put(f"/{name}/{{id}}", status_code=204)
        def update(id: int, body: schema):
            try:
                table.update(body.dict(), doc_ids=[id])
            except KeyError:
                raise HTTPException(status_code=404)
        
        @self.api.delete(f"/{name}/{{id}}", status_code=204)
        def delete(id: int):
            try:
                table.remove(doc_ids=[id])
            except KeyError:
                pass

    def run(self):
        uvicorn.run(self.api)
