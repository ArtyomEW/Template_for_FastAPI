from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title='Trading app')



fake_trades = [
    {'id':1, 'user_id':1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id':2, 'user_id':1, 'currency': 'BTC', 'side': 'sell', 'price': 321, 'amount': 4.15}]

users =[{'id': 1, 'role': 'null', 'name': 'Artyom'}]

class Trade(BaseModel):
    id: int
    user_id: int = Field(ge=0) #id должен быть больше либо равно нулю
    currency: str = Field(max_length=4) #название криптовалюты должно быть не больше 4-ёх букв
    side: str = Field(max_length=3) #название криптовалюты должно быть не больше 4-ёх букв
    price: int = Field(ge=0)  # Цена должна быть больше ли равно нули
    amount: float = Field(ge=0)


class User(BaseModel):
    id: int
    role: str
    name: str


@app.get('/', response_model=List[User])
def get_data(id: int):
    return list(filter(lambda user: user.get('id') == id, users))


@app.post('/add_trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200,
            'data': fake_trades}





