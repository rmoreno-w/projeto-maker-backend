from datetime import datetime

from fastapi import APIRouter, Depends

from controllers.depends.user import get_user_with_role
from models.order import Order
from models.requests.report import ReportData
from models.service_in_order import ServiceInOrder
from models.user import User

router = APIRouter()

@router.post("/balance")
async def get_balance(data_parameters: ReportData,logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
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
            
        total_per_month[f'{month}/{year}'] += float(order.price / 100)

    formatted_data = []
    for month in total_per_month:
        formatted_data.append({'month': month, 'value': total_per_month[month]})

    # print(total_per_month)
    # return {**total_per_month}
    return formatted_data

@router.post("/balance_and_estimation")
async def get_balance_and_estimation(data_parameters: ReportData,logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    # return await Order.objects.select_related('services').filter(solicited_at__gt=datetime(2023,11,24), solicited_at__lt=datetime(2023,11,25)).all()

    initial_date = datetime.fromisoformat(data_parameters.initial_date[:-1])  # Removendo caractere Z da string, nao é aceito no método
    final_date = datetime.fromisoformat(data_parameters.final_date[:-1])  # Removendo caractere Z da string, nao é aceito no método
    
    paid_orders = await Order.objects.filter(solicited_at__gt=initial_date, solicited_at__lte=final_date, payment_status='Paid').order_by('solicited_at').all()
    estimated_orders = await Order.objects.filter(solicited_at__gt=initial_date, solicited_at__lte=final_date, payment_status='Unpaid').order_by('solicited_at').all()

    total_paid_per_month = {}
    for order in paid_orders:
        month = order.solicited_at.month
        year = order.solicited_at.year
        if not f'{month}/{year}' in total_paid_per_month:
            total_paid_per_month[f'{month}/{year}'] = 0
            
        total_paid_per_month[f'{month}/{year}'] += order.price

    total_estimated_per_month = {}
    for order in estimated_orders:
        month = order.solicited_at.month
        year = order.solicited_at.year
        if not f'{month}/{year}' in total_estimated_per_month:
            total_estimated_per_month[f'{month}/{year}'] = 0
            
        total_estimated_per_month[f'{month}/{year}'] += order.price / 100

    # print(total_estimated_per_month)
    return {'paid': {**total_paid_per_month}, 'estimated': {**total_estimated_per_month}}


@router.post("/materials")
async def get_materials_consumed_per_month(data_parameters: ReportData,logged_in_user: User = Depends(get_user_with_role(['admin', 'member']))):
    # return await Order.objects.select_related('services').filter(solicited_at__gt=datetime(2023,11,24), solicited_at__lt=datetime(2023,11,25)).all()

    initial_date = datetime.fromisoformat(data_parameters.initial_date[:-1])  # Removendo caractere Z da string, nao é aceito no método
    final_date = datetime.fromisoformat(data_parameters.final_date[:-1])  # Removendo caractere Z da string, nao é aceito no método

    x = await ServiceInOrder.objects.select_all().filter(order_id__solicited_at__gt=initial_date, order_id__solicited_at__lte=final_date).all()
    # x = await ServiceInOrder.objects.select_all().order_by('id').all()

    consumed_materials = {}
    for service in x:
    # for service in x[::-1]:
        if(service.materials): # Se houver materiais consumidos por um serviço
            for material in service.materials:
                material_object = await material.material_id.load() # Carregar o objeto de material pra pegar o nome, não é carregado por padrao no ormar
                material_name = material_object.name
                month = service.order_id.solicited_at.month
                year = service.order_id.solicited_at.year

                if not f'{material_name}' in consumed_materials: # Se o material analisado ainda n estiver no objeto de materiais consumidos
                    consumed_materials[material_name] = {
                        'unit': material_object.unit,
                        'values':{
                            f'{month}/{year}': 0
                        }
                    }
                
                if not f'{month}/{year}' in consumed_materials[material_name]['values']:
                    consumed_materials[material_name]['values'][f'{month}/{year}'] = 0

                consumed_materials[material_name]['values'][f'{month}/{year}'] += material.quantity
                # if not f'{service.mater}' in consumed_materials:
                # if not f'{month}/{year}' in consumed_materials:
                    # print (material)
        # print(await service.materials[0].material_id.load())
        # break
        # if(len(service.materials)>0):
        #     for consumed_material in service.materials:
        #         print(consumed_material.material_id.name)
    # select_related('service_in_order').all())
    print(consumed_materials)

    formatted_consumed_materials = []
    for key, value in consumed_materials.items():
        formatted_consumed_materials.append({
            'name': key,
            'unit': value['unit'],
            'values': value['values']
        })
    return formatted_consumed_materials