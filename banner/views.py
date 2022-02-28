from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from banner.models import BannerModel
from banner.serializers import BannerSerializer

from datetime import datetime

# Create your views here.

@api_view(['GET','POST','PUT','DELTE'])
def banner_api(request):
    if request.method == 'GET':
        try:
            banners = BannerModel.objects.all()
            banners_serializer = BannerSerializer(banners, many=True)
            return JsonResponse({'banners': banners_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['image'] is None or request_data['distributor_id'] is None:
                return JsonResponse({'success': False, 'error': 'Missing Information'}, status=400)
            banner_data = {
                'image': request_data['image'],
                'distributor_id': request_data['distributor_id'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            banner_serailizer = BannerSerializer(data=banner_data)
            if banner_serailizer.is_valid():
                banner_serailizer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=422)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
