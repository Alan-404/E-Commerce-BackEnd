from category.models import CategoryModel


def get_name_category(category_id):
    category = CategoryModel.objects.get(id=category_id)
    return category.name