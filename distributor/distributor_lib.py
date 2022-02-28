from distributor.models import DistributorModel

def get_user_id_by_distributor(distributor_id):
    distributor = DistributorModel.objects.get(id=distributor_id)
    return distributor.user_id

def get_name_by_id (distributor_id):
    distributor = DistributorModel.objects.filter(id=distributor_id).first()
    return distributor.name