from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

from category.models import CategoryModel
from category.serializers import CategorySerializer

from django.utils import timezone

from datetime import datetime

# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def category_api(request):
    if request.method == 'GET':
        try:
            categories = CategoryModel.objects.all()
            categories_serializer = CategorySerializer(categories, many=True)
            return JsonResponse({'categories': categories_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['name'] == None:
                return JsonResponse({'success': False, 'error': 'Missing information'}, status=400)
            category_data = {
                'name': request_data['name'],
                'description': request_data['description'],
                'thumnail': request_data['thumnail'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            category_serializer = CategorySerializer(data=category_data)
            if category_serializer.is_valid():
                category_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    elif request.method == 'PUT':
        try:
            request_data = JSONParser().parse(request)
            if request_data['description'] is None or request_data['name'] is None or request_data['id'] is None:
                return JsonResponse({'success': False, 'error': 'Missing information'}, status=400)
            category = CategoryModel.objects.get(id=request_data['id'])
            if category is None:
                return JsonResponse({"success": False, 'error': "Invalid category"}, status=404)
            category_data = {
                'name': request_data['name'],
                'description': request_data['description'],
                'thumnail': request_data['thumnail'],
                'created_at': category.created_at,
                'modified_at': datetime.now()
            }
            category_serializer = CategorySerializer(category, data=category_data)
            if category_serializer.is_valid():
                category_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        try:
            category_id = request.query_params['id']
            if category_id is None:
                return JsonResponse({'success': False, 'error': "Invalid category id"}, status=400)
            category = CategoryModel.objects.get(id=category_id)
            if category is None:
                return JsonResponse({'success': False, 'error': 'Invalid category'}, status=400)
            category.delete()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@api_view(['GET'])
def get_category_id(request):
    try:
        category_id = request.query_params['id']
        if category_id is None:
            return JsonResponse({'error': 'Invalid category id'}, status=400)
        category = CategoryModel.objects.get(id=category_id)
        category_serializer = CategorySerializer(category)
        return JsonResponse({'category': category_serializer.data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    
