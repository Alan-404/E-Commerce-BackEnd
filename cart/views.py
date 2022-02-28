from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from cart.models import CartModel
from cart.serializers import CartSerializer

from user import user_lib
from shopping_session import shopping_session_lib
from product import product_lib

from datetime import datetime

# Create your views here.


@api_view(['GET', 'POST', 'DELETE'])
def cart_api (request):
    if request.method == 'GET':
        try:
            carts = CartModel.objects.all()
            carts_serializer = CartSerializer(carts)
            return JsonResponse({'carts': carts_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            user_id = user_lib.get_id_token(request.headers.get('Authorization'))[0]
            if user_id is None or request_data['product_id'] is None or request_data['quantity'] is None:
                return JsonResponse({'success': False, 'error':'Missing Information'}, status=400)
            session_id = shopping_session_lib.get_session_by_user(user_id)[0]
            if session_id is None:
                return JsonResponse({'success': False,'error': 'Invalid Session'}, status=400)
            check_cart = CartModel.objects.filter(session_id = session_id, product_id=request_data['product_id'])
            if check_cart:
                previous_quantity = check_cart[0].quantity
                cart_data = {
                    'session_id': session_id,
                    'product_id': request_data['product_id'],
                    'quantity': request_data['quantity'],
                    'created_at': check_cart[0].created_at,
                    'modified_at': datetime.now()
                }
                cart_serializer = CartSerializer(check_cart[0],data=cart_data)
                if cart_serializer.is_valid():
                    cart_serializer.save()
                else:
                    return JsonResponse({'success': False}, status=500)
                delta_quantity = int(request_data['quantity']) - int(previous_quantity)
                update_total = shopping_session_lib.update_total_of_session(session_id, delta_quantity,request_data['product_id'])
                if update_total == False:
                    return JsonResponse({'success':False},status=500)
                return JsonResponse({'success': True}, status=200)
            cart_data = {
                'session_id': session_id,
                'product_id': request_data['product_id'],
                'quantity': request_data['quantity'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            cart_serializer = CartSerializer(data=cart_data)
            if cart_serializer.is_valid():
                cart_serializer.save()
                update_total = shopping_session_lib.update_total_of_session(session_id,request_data['quantity'] ,request_data['product_id'])
                if update_total == False:
                    return JsonResponse({'success':False},status=500)
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        try:
            user_id = user_lib.get_id_token(request.headers.get('Authorization'))[0]
            cart_id = request.query_params['id']
            if cart_id is None or user_id is None:
                return JsonResponse({'success': False, 'error': 'Invalid id of cart'}, status=400)
            cart = CartModel.objects.get(id=cart_id)
            if cart is None:
                return JsonResponse({'success': False, 'error': "Invalid product in your cart"}, status=400)
            session_id = cart.session_id
            quantity = -cart.quantity
            product_id = cart.product_id
            cart.delete()
            update_total = shopping_session_lib.update_total_of_session(session_id, quantity, product_id)
            if update_total == False:
                return JsonResponse({"success": False}, status=500)
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

""" @api_view(['POST'])
def add_to_cart(request):
    if request.method =='POST':
        try:
            request_data = JSONParser().parse(request)
            user_id = user_lib.get_id_token(request.headers.get('Authorization'))
            if user_id is None or request_data['product_id'] is None:
                return JsonResponse({'error' :'Invalid token'}, status=400)
            
        except Exception as e: """


@api_view(['GET'])
def get_info_cart(request):
    if request.method == 'GET':
        try:
            user_id = user_lib.get_id_token(request.headers.get('Authorization'))[0]
            if user_id is None:
                return JsonResponse({'error': 'Invalid token'})
            (session_id, total) = shopping_session_lib.get_session_by_user(user_id)
            cart = CartModel.objects.filter(session_id=session_id)
            cart_serailizer = CartSerializer(cart, many=True)
            products = []
            
            for item in list(cart):
                products.append(product_lib.get_product_by_id(item.product_id))
            return JsonResponse({'cart': cart_serailizer.data, 'products': products, 'total': total}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)