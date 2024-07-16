from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from operations.router import read_operation


router = APIRouter(prefix='/page',
                   tags=['/pages'])

templates = Jinja2Templates(directory='templates')


@router.get('/base')
async def get_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get("/search/{operation_type}")
def get_search_page(request: Request, operations=Depends(read_operation)):
    return templates.TemplateResponse("search.html", {"request": request, "operations": operations["data"]})


@router.get('/chat')
async def get_chat(request: Request):
    return templates.TemplateResponse('chat.html', {'request': request})

