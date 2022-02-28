from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from shopping_session.models import ShoppingSessionModel
from shopping_session.serializers import ShoppingSessionSerializer

from shopping_session import shopping_session_lib

# Create your views here.

@api_view(['GET', 'POST'])
def shopping_session_api(request):
    if request.method == 'GET':
        try:
            sessions = ShoppingSessionModel.objects.all()
            sessions_serializer = ShoppingSessionSerializer(sessions, many=True)
            return JsonResponse({'sessions': sessions_serializer.data}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'POST':
        try:
            request_data = JSONParser().parse(request)
            if request_data['user_id'] is None:
                return JsonResponse({'success': False, 'error': 'Missing Information'}, status=400)
            add_session = shopping_session_lib.add_session(request_data['user_id'])
            if add_session:
                return JsonResponse({'success': True}, status=200)
            return JsonResponse({'success': False}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
