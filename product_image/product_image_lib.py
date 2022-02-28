from product_image.models import ProductImageModel

def get_thumnail_product(product_id):
    thumnail = ProductImageModel.objects.filter(product_id=product_id, thumnail=True).first()
    return thumnail.image

def get_all_images (product_id):
    images = ProductImageModel.objects.filter(product_id=product_id)
    array_images = []
    for image in list(images):
        array_images.append(image.image)
    return array_images