from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from .models import Message
from database import async_session_maker, get_async_session

router = APIRouter(prefix='/chat')


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_db: bool = False):
        if add_db:
            await self.get_data_for_chat(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def get_data_for_chat(message: str):
        async with async_session_maker() as session:
            query = insert(Message).values(message=message)
            await session.execute(query)
            await session.commit()


manager = ConnectionManager()


@router.get('/last_messages')
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Message).order_by(Message.id.desc()).limit(5)
    result = await session.execute(query)
    return result.scalars().all()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_db=False)




