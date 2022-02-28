from user.models import UserModel
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from user.serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from user import user_lib
from datetime import datetime

from shopping_session import shopping_session_lib
from user_address import user_address_lib
# Create your views here.

@api_view(['GET', 'POST'])
def user_api(request):
    # Check id of admin
    """ try:
        header_authorization = request.headers.get('Authorization')
        if header_authorization is None:
            return JsonResponse({'error': "Not found access token"}, status=403)
        role_id = user_lib.get_id_token(header_authorization)[1]
        if role_id != 1:
            return JsonResponse({'error': "Forbidden"}, status=403)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) """

    # Handle api
    if request.method == 'GET': # get all users
        try:
            header_authorization = request.headers.get('Authorization')
            if header_authorization is None:
                return JsonResponse({'error': "Forbidden"}, status=403)
            
            users = UserModel.objects.all()
            users_serializer = UserSerializer(users, many=True)
            return JsonResponse({"users": users_serializer.data})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    elif request.method == "POST": # add new user
        try:
            request_data = JSONParser().parse(request)
            if request_data["email"] is None or request_data['password'] is None:
                return JsonResponse({"error": "missing information"}, status=400)
            user_data = {
                "email": request_data['email'], 
                'password': make_password(request_data['password']),
                "first_name": request_data["first_name"], 
                'last_name': request_data['last_name'], 
                'telephone': request_data['telephone'], 
                'bdate': request_data['bdate'],
                'gender': request_data['gender'],
                'country': request_data['country'],
                'role_id': request_data['role_id'],
                "avatar": request_data['avatar'],
                'created_at': datetime.now(), 
                'modified_at': datetime.now()
            }
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                add_session = shopping_session_lib.add_session(user_serializer['id'].value)
                if add_session == False:
                    return JsonResponse({"success": False, 'error': 'Invalid user'}, status=400)
                return JsonResponse({"success": True}, status=200)
            return JsonResponse({"success": False}, status=500)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error':str(e)}, status=500)



@api_view(['POST', 'PUT', 'GET'])
def auth_user(request):
    if request.method == 'GET':
        try:
            user_id = user_lib.get_id_token(request.headers.get('Authorization'))[0]
            if user_id is None:
                return JsonResponse({'error': "Invalid token"}, status=400)
            user = UserModel.objects.get(id=user_id)
            user_serializer = UserSerializer(user)
            return JsonResponse({'user': user_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST': # login user
        try:
            request_data = JSONParser().parse(request)
            if request_data['email'] is None or request_data['password'] is None:
                return JsonResponse({'success': False}, status=400)
            user = UserModel.objects.get(email = request_data['email'])
            if user is None:
                return JsonResponse({"success": False, 'error': 'Invalid user'}, status=404)
            if check_password(request_data['password'], user.password):
                access_token = user_lib.make_token(user.id, user.role_id)
                return JsonResponse({'success': True, 'token': access_token}, status=200)
            return JsonResponse({"success": False, "error": "Invalid password"}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    elif request.method == 'PUT': # change password
        try:
            request_data = JSONParser().parse(request)
            if request_data['new_password'] is None or request_data['old_password'] is None:
                return JsonResponse({'success': False, 'error': 'Missing information'}, status=400)
            user_id = user_lib.get_id_token(request.headers.get('Authorization'))[0]
            if user_id is None:
                return JsonResponse({'success': False, 'error': 'Invalid token'}, status=400)
            user = UserModel.objects.get(id=user_id)
            if check_password(request_data['old_password'],user.password) == False:
                return JsonResponse({"success": False, 'error': 'Invalid password'}, status=404)
            if user is None:
                return JsonResponse({'success': False}, status=404)
            UserModel.objects.filter(id=user_id).update(password=make_password(request_data['new_password']), modified_at=datetime.now())
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@api_view(['POST'])
def login_google(request):
    try:
        request_data = JSONParser().parse(request)
        if request_data['email'] is None:
            return JsonResponse({'success': False, 'error': 'Invalid email'}, status=400)
        user = UserModel.objects.get(email=request_data['email'])
        token = user_lib.make_token(user.id, user.role_id)
        return JsonResponse({'success': True, 'token': token}, status=200)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@api_view(['GET'])
def get_profile(request):
    try:
        user_id = user_lib.get_id_token(request.headers.get('Authorization'))[0]
        if user_id is None:
            return JsonResponse({'error':'Invalid Token'})
        user = UserModel.objects.get(id=user_id)
        addresses = user_address_lib.get_addresses(user_id)
        user_serializer = UserSerializer(user)
        return JsonResponse({'user': user_serializer.data, 'addresses': addresses}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    
    