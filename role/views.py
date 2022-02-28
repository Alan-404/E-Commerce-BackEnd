from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from user import user_lib

from role.models import RoleModel
from role.serializers import RoleSerializer

from datetime import datetime

# Create your views here.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def role_api (request):
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
            roles = RoleModel.objects.all()
            roles_serializer = RoleSerializer(roles, many=True)
            return JsonResponse({'roles': roles_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['name'] is None:
                return JsonResponse({'success': False, 'error': 'Missing information'}, status=400)
            role_data = {
                'name': request_data['name'],
                'created_at': datetime.now(),
                'modified_at': datetime.now()
            }
            role_serializer = RoleSerializer(data=role_data)
            if role_serializer.is_valid():
                role_serializer.save()
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
