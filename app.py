from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel


class User(BaseModel):
    username: str | None = None
    email: str
    password: str
    messages: list

class Message(BaseModel):
    message: str
    sender: str
    sender_email: str
    receiver_id: int


app = FastAPI()

db_array = []

db = "db.json"


def load_data_json():
    with open(db, 'r') as file:
        print(file)
        return json.load(file)


def signup(user_signup):
    data = load_data_json()
    for user in data:
        if (user['email'] == user_signup.email) or (user['username'] == user_signup.username):
            print("user already exists")
            return "User Already Exists"

    new_user = {
        "user_id": len(data)+1,
        "email": user_signup.email,
        "username": user_signup.username,
        "password": user_signup.password,
        "messages": []
    }
    data.append(new_user)
    with open(db, 'w') as file:
        json.dump(data, file)
    return "sign Up successful"


def login_json(user_data):
    data = load_data_json()
    for user in data:
        if user["email"] == user_data.email:
            if user["password"] == user_data.password:
                print("LOGIN!!")
                return user
            else:
                return "Wrong Password"


def add_message(message):
    data = load_data_json()
    for user in data:
        if user['user_id'] == message.receiver_id:
            message_info = {
                "message": message.message,
                "sender-email": message.sender_email,
                "sender-name": message.sender
            }
            user['messages'].append(message_info)
            with open(db, 'w') as file:
                json.dump(data, file)

@app.get("/")
def root():
    return {"message": "a"}


@app.get("/users/{id}")
def get_user(id: int):
    a = db[id]
    return a

@app.post("/signup")
def create_user(user: User):
    signup(user)
    return user

@app.post("/login")
def login(user: User):
    return login_json(user)


@app.post("/message")
def message(message: Message):
    return add_message(message=message)