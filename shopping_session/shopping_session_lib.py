from shopping_session.models import ShoppingSessionModel
from shopping_session.serializers import ShoppingSessionSerializer

from datetime import datetime
from product import product_lib

def add_session(user_id):
    session_data = {
        'id': str(datetime.now()),
        'user_id': user_id
    }
    session_serializer = ShoppingSessionSerializer(data=session_data)
    if session_serializer.is_valid():
        session_serializer.save()
        return True
    return False

def get_session_by_user (user_id):
    session = ShoppingSessionModel.objects.get(user_id=user_id)
    return (session.id, session.total)

def update_total_of_session (session_id, delta_quantity, product_id):
    session = ShoppingSessionModel.objects.get(id=session_id)
    if session is None:
        return False
    price = product_lib.get_price_of_product(product_id)
    total = float(session.total) + float(price)*float(delta_quantity)
    ShoppingSessionModel.objects.filter(id=session_id).update(total=total)
    return True

def get_total(session_id):
    return ShoppingSessionModel.objects.filter(id=session_id).first['total']
    