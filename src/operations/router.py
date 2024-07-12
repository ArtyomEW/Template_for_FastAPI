from time import sleep

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import insert, select, update, delete
from .model_operatiom import Operation
from .schema import OperationAdd
from fastapi_cache.decorator import cache

router = APIRouter(prefix='/Operations',
                   tags=['Operations'])


@router.get('/read_opeariton')
@cache(expire=10)
async def read_operation(session: AsyncSession = Depends(get_async_session)):
    sleep(3)
    query = select(Operation)
    result = await session.execute(query)
    return {'status': 200,
            'data': result.mappings().all(),
            'detail': None}


@router.post('/add_operation')
async def add_operation(schema: OperationAdd, session: AsyncSession = Depends(get_async_session)):
    query = insert(Operation).values(**schema.dict())
    try:
        await session.execute(query)
        await session.commit()
        return {'status': 200,
                'data': None,
                'detail': 'Вы успешно добавили операции'}
    except Exception:
        raise HTTPException(status_code=500, detail={
            'data': None,
            'detail': 'Что то пошло не так. Возможно вы не указали все данные для всех полей'
        })


@router.put('/update_operation')
async def update_operation(schema: OperationAdd, session: AsyncSession = Depends(get_async_session)):
    try:
        query = update(Operation).values(**schema.dict()).where(Operation.id == schema.id)
        await session.execute(query)
        await session.commit()
        return {'status': 200,
                'data': None,
                'detail': 'Успешно вы обновили данные под вашим идентификатором'}
    except Exception:
        raise HTTPException(status_code=500, detail={
            'data': None,
            'detail': 'Вы возможно не правильно указали идентификатор'
        })


@router.delete('/delete_operation')
async def delete_operation(id_operation: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = delete(Operation).where(Operation.id == id_operation)
        await session.execute(query)
        await session.commit()
        return {'status': 200,
                'data': None,
                'detail': 'Успешно вы удалили данные под вашим идентификатором'}
    except Exception:
        raise HTTPException(status_code=500, detail={
            'data': None,
            'detail': 'Возможно вы указали не правильный идентификатор'
        })

