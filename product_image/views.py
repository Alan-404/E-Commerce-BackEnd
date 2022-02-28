from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from product_image.models import ProductImageModel
from product_image.serializers import ProductImageSerializer

from datetime import datetime

# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def product_image_api (request):
    if request.method == 'GET':
        try:
            images = ProductImageModel.objects.all()
            images_serializer = ProductImageSerializer(images, many=True)
            return JsonResponse({'images': images_serializer.data},status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['product_id'] is None or request_data['image'] is None:
                return JsonResponse({'success': False, 'error': 'Missing Information'}, status=400)
            image_data = {
                'product_id': request_data['product_id'],
                'image': request_data['image'],
                'thumnail': False,
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            image_serializer = ProductImageSerializer(data=image_data)
            if image_serializer.is_valid():
                image_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=500)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    elif request.method == "PUT":
        try:
            request_data = JSONParser().parse(request)
            if request_data['id'] is None:
                return JsonResponse({'success': False, 'error': "Missing Information"}, status=400)
            image = ProductImageModel.objects.get(id=request_data['id'])
            if image is None:
                return JsonResponse({'success': False, 'error': 'Not Found Image'}, status=400)
            image_data = {
                'product_id': request_data['product_id'],
                'image_id': request_data['image'],
                'created_at': image.created_at,
                'modified_at': datetime.now()
            }
            image_serializer = ProductImageSerializer(image, data=image_data)
            if image_serializer.is_valid():
                image_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False},status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        try:
            image_product_id = request.query_params['id']
            if image_product_id is None:
                return JsonResponse({'success': False, 'error': "Invalid Id"}, status=400)
            image = ProductImageModel.objects.get(id=image_product_id)
            if image is None:
                return JsonResponse({'success': False, 'error': 'Not Found'}, status=400)
            image.delete()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@api_view(['PUT'])
def active_thumnail(request):
    try:
        request_data = JSONParser().parse(request)
        if request_data['id'] is None:
            return JsonResponse({'success': False}, status=400)
        image = ProductImageModel.objects.get(id=request_data['id'])
        thumnail = ProductImageModel.objects.filter(product_id=image.product_id, thumnail=True).first()
        if thumnail is not None:
            thumnail_data = {
                'product_id': image.product_id,
                'image': thumnail.image,
                'thumnail': False,
                'created_at': thumnail.created_at,
                'modified_at': datetime.now()
            }
            thumnail_serializer = ProductImageSerializer(thumnail, data=thumnail_data)
            if thumnail_serializer.is_valid():
                thumnail_serializer.save()
        image_data = {
            'product_id': image.product_id,
            'image': image.image,
            'thumnail': True,
            'created_at': image.created_at,
            'modified_at': datetime.now()
        }
        image_serializer = ProductImageSerializer(image, data=image_data)
        if image_serializer.is_valid():
            image_serializer.save()
            return JsonResponse({'success': True}, status=200)
        return JsonResponse({'success': False}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@api_view(['GET'])
def get_images_product(request):
    if request.method == 'GET':
        try:
            product_id = request.query_params['id']
            images = ProductImageModel.objects.filter(product_id=product_id);
            images_serializer = ProductImageSerializer(images, many=True)
            return JsonResponse({'images': images_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)