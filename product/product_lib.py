from product.models import ProductModel
from discount import discount_lib
from distributor import distributor_lib
from product_image import product_image_lib

def get_price_of_product(product_id):
    discount_percent = discount_lib.get_discount_of_product(product_id)
    discount_value = 0;
    if discount_percent['active'] == True:
        discount_value = discount_percent['discount_percent']
    product = ProductModel.objects.get(id=product_id)
    price = ((100-discount_value)/100)*product.price
    return round(price, 3)

def get_product_by_id (product_id):
    product = ProductModel.objects.get(id=product_id)
    discount = discount_lib.get_discount_of_product(product.id)
    distributor = distributor_lib.get_name_by_id(product.distributor_id)
    thumnail = product_image_lib.get_thumnail_product(product_id)
    product_data = {
        "id": product_id,
        'name': product.name,
        'price': product.price,
        'discount_percent': discount['discount_percent'],
        'active': discount['active'],
        'distributor': distributor,
        'thumnail': thumnail
    }
    return product_data;
