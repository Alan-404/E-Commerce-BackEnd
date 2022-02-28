from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from product_inventory.models import ProductInventoryModel
from product_inventory.serializers import ProductInventorySerializer

from datetime import datetime

# Create your views here.


@api_view(['GET', 'POST'])
def product_inventory_api (request):
    if request.method == 'GET':
        try:
            inventories = ProductInventoryModel.objects.all()
            inventories_serializer = ProductInventorySerializer(inventories, many=True)
            return JsonResponse({'inventories': inventories_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['product_id'] is None or request_data['quantity'] is None:
                return JsonResponse({'success': False, 'error': 'Missing Information'}, status=400)
            inventory_data = {
                'product_id': request_data['product_id'],
                'quantity': request_data['quantity'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            inventory_serializer = ProductInventorySerializer(data=inventory_data)
            if inventory_serializer.is_valid():
                inventory_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
