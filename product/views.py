from django.http import JsonResponse
from matplotlib.image import thumbnail
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from product.models import ProductModel
from product.serializers import ProductSerializer

from distributor import distributor_lib
from datetime import datetime

from category import category_lib
from product_image import product_image_lib
from distributor import distributor_lib
from discount import discount_lib

# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def product_api (request):
    if request.method == 'GET':
        try:
            products = ProductModel.objects.all()
            products_serializer = ProductSerializer(products, many=True)
            return JsonResponse({'products': products_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['name'] is None or request_data['price'] is None or request_data['category_id'] is None or request_data['distributor_id'] is None:
                return JsonResponse({'success': False, 'error': "Missing Information"}, status=400)
            user_id = distributor_lib.get_user_id_by_distributor(request_data['distributor_id'])
            if user_id is None:
                return JsonResponse({'success': False, 'error': "Not Found User"}, status=400)
            sum_part = 3
            category_id = (sum_part - len(str(request_data['category_id'])))*"0" + str(request_data['category_id'])
            distributor_id = (sum_part - len(str(request_data['distributor_id'])))*"0" + str(request_data['distributor_id'])
            user_id = (sum_part - len(str(user_id)))*"0" + str(user_id)

            sku_code = category_id + distributor_id + user_id
            product_data = {
                'name': request_data['name'],
                'description': request_data['description'],
                'price': request_data['price'],
                'sku': sku_code,
                'category_id': request_data['category_id'],
                'distributor_id': request_data['distributor_id'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            product_serializer = ProductSerializer(data=product_data)
            if product_serializer.is_valid():
                product_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)



@api_view(['GET'])
def get_products_dashboard(request):
    try:
        products = ProductModel.objects.all()[:10]
        categories = []
        thumnails = []
        distributors= []
        discounts = []
        for product in list(products):
            categories.append(category_lib.get_name_category(product.category_id))
            thumnails.append(product_image_lib.get_thumnail_product(product.id))
            distributors.append(distributor_lib.get_name_by_id(product.distributor_id))
            discounts.append(discount_lib.get_discount_of_product(product.id))
        products_serializer = ProductSerializer(products, many=True)
        return JsonResponse({'products': products_serializer.data, 'categories': categories, 'thumnails': thumnails, 'distributors': distributors, 'discounts': discounts}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@api_view(['GET'])
def get_products_category (request):
    try:
        category_id = request.query_params['id']
        index = int(request.query_params['index'])
        thumnails = []
        distributors= []
        discounts = []
        if index is None:
            return JsonResponse({'error': 'Invalid index to start'}, status=400)
        products = ProductModel.objects.filter(category_id=category_id)[(index-1)*10:index+10]
        for product in list(products):
            thumnails.append(product_image_lib.get_thumnail_product(product.id))
            distributors.append(distributor_lib.get_name_by_id(product.distributor_id))
            discounts.append(discount_lib.get_discount_of_product(product.id))
        products_serializer = ProductSerializer(products, many=True)
        return JsonResponse({'products': products_serializer.data, "thumnail": thumnails, "distributors": distributors, "discounts": discounts}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)})

@api_view(['GET'])
def get_product_id(request):
    if request.method == 'GET':
        try:
            product_id = request.query_params['id']
            if product_id is None:
                return JsonResponse({'error': 'Invalid token'}, status=400)
            product = ProductModel.objects.get(id=product_id)
            product_serializer = ProductSerializer(product)
            return JsonResponse({"product": product_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)})