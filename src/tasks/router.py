from fastapi import APIRouter, Depends, HTTPException
from auth.base_config import current_user

from .tasks import send_email_report


router = APIRouter(
    prefix='/send_letter',
    tags=['send_letter']
)


@router.get('/send_letter')
def send_letter(user=Depends(current_user)):
    try:
        send_email_report.delay(user.username)
        return {'status': 200,
                'data': 'Письмо отправлено',
                'detail': None
                }
    except Exception:
        raise HTTPException(status_code=400, detail={
            'status': 'error',
            'data': None,
            'detail': 'Войдите в наше веб приложение'
        })
