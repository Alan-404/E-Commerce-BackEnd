from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.db import connection

from discount.models import DiscountModel
from discount.serializers import DiscountSerializer

from datetime import datetime
# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def discount_api (request):
    #Check access token

    #Handle api
    if request.method == 'GET':
        try:
            discounts = DiscountModel.objects.all()
            discounts_serializer = DiscountSerializer(discounts, many=True)
            return JsonResponse({'discounts': discounts_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['product_id'] is None or request_data['discount_percent'] is None:
                return JsonResponse({'success': False, 'error': "Missing Informaion"}, status=400)
            discount_data = {
                'product_id': request_data['product_id'],
                'discount_percent': request_data['discount_percent'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            discount_serializer = DiscountSerializer(data=discount_data)
            if discount_serializer.is_valid():
                discount_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    elif request.method == 'PUT':
        try:
            request_data = JSONParser().parse(request)
            if request_data['product_id'] is None or request_data['discount_percent'] is None or request_data['active'] is None or request_data['id'] is None:
                return JsonResponse({'success': False, 'error': 'Missing Information'}, status=400)
            discount = DiscountModel.objects.get(id=request_data['id'])
            if discount is None:
                return JsonResponse({'success': False, 'error': "Not Found"}, status=404)
            discount_data = {
                'product_id': request_data['product_id'],
                'discount_percent': request_data['discount_percent'],
                'active': request_data['active'],
                'created_at': discount.created_at,
                'modified_at': datetime.now()
            }
            discount_serializer = DiscountSerializer(discount, data=discount_data)
            if discount_serializer.is_valid():
                discount_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@api_view(['GET'])
def get_discount_of_product(request):
    if request.method == 'GET':
        try:
            product_id = request.query_params['id']
            discount = DiscountModel.objects.get(product_id=product_id)
            discount_serializer = DiscountSerializer(discount)
            return JsonResponse({'discount': discount_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



