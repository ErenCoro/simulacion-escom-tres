from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse



from .models import *

################ Authentication
users_db = {
    "TestUser": {
        "username": "TestUser",
        "hashed_password": "&TestUserPassword123.",
    },
}

app = FastAPI()


def hash_password(password: str):
    return  password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    
class UserInDB(User):
    hashed_password: str

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


################## Models

class linear_regression(BaseModel):
    data_url: str
    learning_rate: float
    iterations: int

class prediction_linear(BaseModel):
    model_weights: list
    input_data: list
  

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user_dict = users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    #UserInDB(**user_dict) means: Pass the keys and values of the user_dict directly as key-value arguments
    user = UserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.post("/linear/regression/sgd/train")
async def link(*, token: str = Depends(oauth2_scheme), data: linear_regression):
    url = data.data_url
    learning = data.learning_rate
    iteration = data.iterations
    output = train_SGDR(url, learning, iteration)
    json_compatible_item_data = jsonable_encoder(output)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/linear/regression/sgd/predict")
async def link(*, token: str = Depends(oauth2_scheme), data: prediction_linear):
    weights = data.model_weights
    data = data.input_data
    output = test_SGDR(weights, data)
    json_compatible_item_data = jsonable_encoder(output)
    return JSONResponse(content=json_compatible_item_data)


