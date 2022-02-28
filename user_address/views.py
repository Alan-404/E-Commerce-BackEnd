from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from user_address.models import UserAddressModel
from user_address.serializers import UserAddressSerializer

from datetime import datetime

from user import user_lib

# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def user_address_api(request):
    # Check valid admin
    try:
        header_authorization = request.headers.get('Authorization')
        if header_authorization is None:
            return JsonResponse({'error': "Not found access token"}, status=403)
        role_id = user_lib.get_id_token(header_authorization)[1]
        if role_id != 1:
            return JsonResponse({'error': 'Forbidden'}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Handle api
    if request.method == 'GET':
        try:
            addresses = UserAddressModel.objects.all()
            addresses_serializer = UserAddressSerializer(addresses, many=True)
            return JsonResponse({'addresses': addresses_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST': # add address from admin
        try:
            request_data = JSONParser().parse(request)
            if request_data['user_id'] is None or request_data['address'] is None:
                return JsonResponse({'success': False, 'error': 'Missing information'}, status=400)
            address_data = {
                'user_id': request_data['user_id'],
                'address': request_data['address'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            address_serializer = UserAddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def address_user_side(request): # Need access token
    # Check valid id of user
    user_id = None
    try:
        user_id = user_lib.get_id_token(request.headers.get('Authorization'))[0]
        if user_id is None:
            return JsonResponse({'success': False, 'error': 'Invalid id of user'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    # Handle api
    if request.method == 'GET':
        try:
            addresses = UserAddressModel.objects.filter(user_id=user_id)
            addresses_serializer = UserAddressSerializer(addresses, many=True)
            return JsonResponse({'addresses': addresses_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data["address"] is None:
                return JsonResponse({'success': False, 'error': "Missing information"}, status=400)
            address_data = {
                'user_id': user_id,
                'address': request_data['address'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            address_serializer = UserAddressSerializer(data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, 'error': str(e)}, status=500)
    elif request.method == 'PUT':
        try:
            request_data = JSONParser().parse(request)
            if request_data['address'] is None:
                return JsonResponse({'success': False, 'error': 'Missing informaion'}, status=400)
            address = UserAddressModel.objects.get(id=request_data['id'])
            if address is None:
                return JsonResponse({'success': False, 'error': 'Invalid address'}, status=400)
            if address.user_id != user_id:
                return JsonResponse({'success': False, 'error': 'It is not your address'}, status=403)
            address_data = {
                'user_id': user_id,
                'address': request_data['address'],
                'created_at': address.created_at,
                'modified_at': datetime.now()
            }
            address_serializer = UserAddressSerializer(address, data=address_data)
            if address_serializer.is_valid():
                address_serializer.save()
                return JsonResponse({"success": True}, status=200)
            return JsonResponse({'success': False}, status=500)
        except Exception as e:
            return JsonResponse({'success': False}, status=500)
    else:
        try:
            address_id = request.query_params['id']
            if address_id is None:
                return JsonResponse({'success': False, 'error': "Invalid id of address"}, status=400)
            address = UserAddressModel.objects.get(id=address_id)
            if address is None:
                return JsonResponse({'success': False, 'error': 'Invalid address'}, status=400)
            if address.user_id != user_id:
                return JsonResponse({'success': False, 'error': 'It is not your address'}, status=403)
            address.delete()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': True, 'error': str(e)}, status=500)
        
