from fastapi import FastAPI

app = FastAPI(title='Trading app')



users = [
    {'id':1, 'name': 'Nikita','surname': 'Nikiforenko'},
    {'id':2, 'name': 'Oleg','surname': 'Makarov'}
        ]


@app.get('/give_user')
def get_user(id: int):
    return [user for user in users if id == user.get('id')]


@app.post('/user')
def insert_user(user_id: int, name: str, surname: str):
    user = list(filter(lambda user: user.get('id') == user_id, users))[0]
    user['name'] = name
    user['surname'] = surname
    return {'data_user': user,
            'data': users}

#uvicorn main:app --reload


