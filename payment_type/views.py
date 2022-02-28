from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from payment_type.models import PaymentTypeModel
from payment_type.serializers import PaymentTypeSerializer

# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def payment_type_api (request):
    if request.method == 'GET':
        try:
            payment_types = PaymentTypeModel.objects.all()
            payment_types_serializer = PaymentTypeSerializer(payment_types, many=True)
            return JsonResponse({'types': payment_types_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['type_name'] is None:
                return JsonResponse({'success': False, 'error': 'Missing Information'}, status=400)
            type_data = {
                'type_name': request_data['type_name'],
                'description': request_data['description']
            }
            payment_type_serializer = PaymentTypeSerializer(data=type_data)
            if payment_type_serializer.is_valid():
                payment_type_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    elif request.method == 'PUT':
        try:
            request_data = JSONParser().parse(request)
            if request_data['type_name'] is None or request_data['description'] is None or request_data['id'] is None:
                return JsonResponse({'success': False, 'error': 'Missing Information'}, status=400)
            payment_type = PaymentTypeModel.objects.get(id=request_data['id'])
            if payment_type is None:
                return JsonResponse({'success': False, 'error': 'Type of Payment Not Found'}, status=404)
            type_data = {
                'type_name': request_data['type_name'],
                'description': request_data['description']
            }
            type_serializer = PaymentTypeSerializer(payment_type, data=type_data)
            if type_serializer.is_valid():
                type_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)