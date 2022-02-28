from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from order_detail.models import OrderDetailModel
from order_detail.serializers import OrderDetailSerializer

# Create your views here.

@api_view(['GET', 'POST', 'PUT','DELETE'])
def order_detail_api (request):
    if request.method == 'GET':
        try:
            orders = OrderDetailModel.objects.all()
            orders_serializer = OrderDetailSerializer(orders, many=True)
            return JsonResponse({'orders': orders_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    ''' elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if 
        except Exception as e: '''
