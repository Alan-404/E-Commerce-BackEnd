from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from distributor.models import DistributorModel
from distributor.serializers import DistributorSerializer

from datetime import datetime
from user import user_lib

# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def distributor_api(request):
    # Check admin
    try:
        header_authorization = request.headers.get('Authorization')
        if header_authorization is None:
            return JsonResponse({'error': "Not found access token"}, status=403)
        role_id = user_lib.get_id_token(header_authorization)[1]
        if role_id != 1:
            return JsonResponse({"error": "Forbidden"}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Handle api
    if request.method == 'GET':
        try:
            distributors = DistributorModel.objects.all()
            distributors_serializer = DistributorSerializer(distributors, many=True)
            return JsonResponse({'distributors': distributors_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['user_id'] is None:
                return JsonResponse({'success': False, 'error': "Missing id of user"}, status=400)
            distributor_data = {
                'name': request_data['name'],
                'user_id': request_data['user_id'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            distributor_serializer = DistributorSerializer(data=distributor_data)
            if distributor_serializer.is_valid():
                distributor_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    elif request.method == 'PUT':
        try:
            request_data = JSONParser().parse(request)
            if request_data['id'] is None:
                return JsonResponse({'success': False, 'error': 'Invalid id of distributor'}, status=400)
            distributor = DistributorModel.objects.get(id=request_data['id'])
            if distributor is None:
                return JsonResponse({'success': False, 'error': 'Invalid distributor'})
            distributor_data = {
                'name': request_data['name'],
                'user_id': request_data['user_id'],
                'created_at': distributor.created_at,
                'modified_at': datetime.now()
            }
            distributor_serializer = DistributorSerializer(distributor, data=distributor_data)
            if distributor_serializer.is_valid():
                distributor_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        try:
            distributor_id = request.query_params['id']
            if id is None:
                return JsonResponse({'success': False, 'error': "Invalid id"}, status=400)
            distributor = DistributorModel.objects.get(id=distributor_id)
            if distributor is None:
                return JsonResponse({'success': False, 'error': "Distributor not found"}, status=404)
            distributor.delete()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@api_view(['GET'])
def get_distributor(request):
    if request.method == 'GET':
        try:
            distributor_id = request.query_params['id']
            distributor = DistributorModel.objects.get(id=distributor_id)
            distributor_serializer = DistributorSerializer(distributor)
            return JsonResponse({'distributor': distributor_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)