from datetime import datetime

from fastapi import APIRouter, Depends

from controllers.depends.user import get_user_with_role
from models.order import Order
from models.requests.report import ReportData
from models.user import User

router = APIRouter()

@router.post("/balance")
async def get_materials(data_parameters: ReportData,logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    # return await Order.objects.select_related('services').filter(solicited_at__gt=datetime(2023,11,24), solicited_at__lt=datetime(2023,11,25)).all()

    initial_date = datetime.fromisoformat(data_parameters.initial_date[:-1])  # Removendo caractere Z da string, nao é aceito no método
    final_date = datetime.fromisoformat(data_parameters.final_date[:-1])  # Removendo caractere Z da string, nao é aceito no método
    
    orders = await Order.objects.filter(solicited_at__gt=initial_date, solicited_at__lte=final_date, payment_status='Paid').order_by('solicited_at').all()

    total_per_month = {}
    for order in orders:
        month = order.solicited_at.month
        year = order.solicited_at.year
        if not f'{month}/{year}' in total_per_month:
            total_per_month[f'{month}/{year}'] = 0
            
        total_per_month[f'{month}/{year}'] += order.price

    # print(total_per_month)
    return {**total_per_month}
