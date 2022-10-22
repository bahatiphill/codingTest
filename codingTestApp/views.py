from .models import Users
from django.core import serializers
from django.core.cache import cache
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from .utils import validate_data, getDataFromExcel
from django.views.decorators.csrf import csrf_exempt
from .tasks import process_data_from_excel, save_data_to_db
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view


def home(request):
    """
    Return Ok to notify that the application is running
    Doesn't require user to be authenticated
    """
    return JsonResponse({'status': 'ok','description': 'app is running'})



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def upload_users_file(request):
    """
    1. Get uploaded excel file
    2. Check any malformation 
    3. Validate the file
    4. Save the data to In memory Redis instance
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



@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def users_list(request):
    """
    Show the validated users in redis Instance
    """
    print('running')
    data = cache.get("USERS")
    if data is None:
        return JsonResponse({'status': 'error', 'description':'There is no data yet'})
    return JsonResponse({'status':'ok', 'data': data})



@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def commit_to_db(request):
    """
    Save Validated users in redis instance to Database
    """
    
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




@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def savedUsers(request):

    """
    Return saved users in the database
    """
    users = Users.objects.all()
    qs_json = serializers.serialize('json', users)
    return HttpResponse(qs_json, content_type='application/json')

