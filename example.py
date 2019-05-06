from tinycrud import TinyCRUD
from pydantic import BaseModel

class User(BaseModel):
    email: str
    username: str
    age: int
    password: str

app = TinyCRUD()
app.collection("users", User)
app.run()
