from user_address.models import UserAddressModel

def get_addresses(user_id):
    addresses = UserAddressModel.objects.filter(user_id=user_id)
    array_addresses = []
    for address in list(addresses):
        array_addresses.append(address.address)
    return array_addresses