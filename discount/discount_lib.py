from discount.models import DiscountModel

def get_discount_of_product (product_id):
    discount = DiscountModel.objects.filter(product_id=product_id).first()
    discount_data = {
        "discount_percent": discount.discount_percent,
        "active": discount.active
    }
    return discount_data;