from django.core.cache import cache
from .models import Users
from celery import shared_task
from .utils import validate_data, getDataFromExcel
import io
import base64


# TODO : Serialize excel object to make this function work
@shared_task()
def process_data_from_excel(excel_file_base64):

    uploaded_file = base64.b64decode(excel_file_base64)

    print("TODO")
    data_ = getDataFromExcel(uploaded_file)
    validated_data = validate_data(data_)
    print("validated_data: ", validated_data)
    cache.set("USERS", validated_data)
    return {"status": True}


@shared_task()
def save_data_to_db(data):

    for item in data:
            Users.objects.create(
                names = item.get('names'),
                nid = item.get('nid'),
                phone_number = item.get('phone_number'),
                gender = item.get('gender'),
                email = item.get('email'),
                phone_valid = item.get('phone_valid'),
                nid_valid = item.get('nid_valid'),
                email_valid = item.get('email_valid')
            )