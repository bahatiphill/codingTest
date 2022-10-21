from .models import Users
from django.core import serializers
from django.core.cache import cache
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from .utils import validate_data, getDataFromExcel
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_data_from_excel, save_data_to_db



def home(request):
    """
    Desc:
    """
    return JsonResponse({'status': 'ok','description': 'app is running'})


@csrf_exempt
def upload_users_file(request):
    """
    """
    if request.method == 'POST':
        
        uploaded_file = request.FILES.get('usersfile')
        print('file: ', uploaded_file)

        #Check If file is provided
        if  uploaded_file == None:
            result = {'status': 'error','description': 'No Excel file provided'}
            return JsonResponse(result)

        #Check If provided file is an excel file.
        if not uploaded_file.name.endswith('.xlsx'):
            result = {'status': 'error','description': 'Please provide an excel file'}
            return JsonResponse(result)

        #TODO:Send data validation to Clery background task
        #process_data_from_excel.delay(uploaded_file)


        #Open file and store content in Redis instance
        data_ = getDataFromExcel(uploaded_file)
        validated_data = validate_data(data_)
        print("validated_data: ", validated_data)
        cache.set("USERS", validated_data)

        return JsonResponse({'status': 'ok', 'description':' Data uploaded, records are being validated'})


    else:
        result = {
            'status': 'error',
            'description': 'Use POST to upload the excel file'
        }
        return JsonResponse(result)


def users_list(request):
    data = cache.get("USERS")
    if data is None:
        return JsonResponse({'status': 'error', 'description':'There is no data yet'})
    return JsonResponse({'status':'ok', 'data': data})


@csrf_exempt
def commit_to_db(request):
    
    if request.method == 'POST':

        data = cache.get('USERS')
        if data is None:
            return JsonResponse({'status': 'error', 'description':'There no data to commit to DB yet'})

        # Call Celery background job to save data
        save_data_to_db.delay(data)

        cache.delete('USERS')
        return JsonResponse({'status': 'ok', 'description':'saved to DB'})

    if request.method == 'GET':
        return JsonResponse({'status': 'error', 'description':'use POST please'})


def savedUsers(request):
    users = Users.objects.all()
    qs_json = serializers.serialize('json', users)
    return HttpResponse(qs_json, content_type='application/json')

