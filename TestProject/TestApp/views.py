# Create your views here.
import datetime
import re

from TestApp.utils import *
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from django.template import loader
from rest_framework.decorators import api_view

from .decorators import *
from .enums import UserRole
from .models import Users

logger = logging.getLogger(__name__)


# def login(request):
#     template = loader.get_template('login.html')
#     name = {
#         'user': 'rahul'
#     }
#     return HttpResponse(template.render(name))


def signup(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render())


@api_view(['POST'])
def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    return HttpResponse("<h2>Hello, Welcome to Django!</h2>")


@api_view(['POST'])
def create_user(request):
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    photo_url = request.POST['p_url']

    if not re.match(r"(^([^\s@]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})$)", email):
        return HttpResponse("<h2>Please Enter Valid Email</h2>")
    if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        return HttpResponse(
            "<h2>Password should be minimum 8 character</h2>")
    if Users.objects.values("id").filter(email=email):
        return HttpResponse("<h2>User already exists. Please sign in with your credentials</h2>")

    instance = Users.objects.create(first_name=first_name, last_name=last_name, email=email,
                                    password=encode_string(password),
                                    photo_url=photo_url, role_id=2)
    template = loader.get_template('welcome.html')
    name = {
        'user': first_name + " " + last_name
    }
    return HttpResponse(template.render(name))


@api_view(["POST"])
def signin_user(request):
    email = request.data["email"]
    password = request.data['password']
    if not re.match(r"(^([^\s@]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})$)", email):
        return HttpResponse(json.dumps(HttpErrorHandler.invalid_email()), content_type="application/json")
    if not re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        return HttpResponse(json.dumps(HttpErrorHandler.invalid_password()), content_type="application/json")
    data = Users.objects.filter(Q(email=email) & Q(password=encode_string(password)))
    if not data:
        return HttpResponse(json.dumps(HttpErrorHandler.invalid_authentication()), content_type="application/json")
    token = jwt.encode({
        'user': email,
        'password': password,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, os.environ.get("JWT_SECRET_KEY", "xyz")
    )
    return JsonResponse({'token': token})


@login_required_and_get_request_parameter
def user_list(**kwargs):
    try:
        page = int(kwargs['page'])
        limit = int(kwargs['limit'])
        data = Users.objects.values("id", "email").filter(id__range=[page, page + limit]).order_by('id')[:limit]
        user_list_response['user_list'] = list(data)
        return HttpResponse(json.dumps(user_list_response), content_type="application/json")
    except:
        return HttpResponse(json.dumps(HttpErrorHandler.application_error()), content_type="application/json")


def get_user_details(id):
    return Users.objects.values("id", "email", full_name=Concat('first_name', Value(' '), 'last_name')).filter(
        id=id)


@api_view(["GET"])
@login_required_and_get_request_parameter
def user_details(**kwargs):
    if not kwargs['id']:
        logger.error("Get data Using login user")
        data = Users.objects.values(
            "id", "email", full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(Q(email=kwargs['user_data']['user']) & Q(password=encode_string(kwargs['user_data']['password'])))
        user_details_response['details'] = list(data)
    else:
        kwargs['id'] = int(kwargs['id'])
        logger.error("Get data Using ID")
        data = list(Users.objects.values("id", "email", 'role_id').filter(email=kwargs['user_data']['user']))
        if data[0]['role_id'] == UserRole.ADMIN.value:
            logger.error("User is Admin")
            if not list(get_user_details(kwargs['id'])):
                return HttpResponse(json.dumps(HttpErrorHandler.resource_not_found_error()),
                                    content_type="application/json")
            user_details_response['details'] = list(get_user_details(kwargs['id']))
        else:
            logger.error("User is Normal")
            logger.error(
                "Database id: {db_id} and query parameter id: {param_id}".format(db_id=data[0]['id'], param_id=kwargs['id']))
            if not list(get_user_details(kwargs['id'])):
                return HttpResponse(json.dumps(HttpErrorHandler.resource_not_found_error()),
                                    content_type="application/json")
            if data[0]['id'] == kwargs['id']:
                user_details_response['details'] = list(get_user_details(kwargs['id']))
            else:
                return HttpResponse(json.dumps(HttpErrorHandler.insufficient_permission_error()),
                                    content_type="application/json")
    return HttpResponse(json.dumps(user_details_response), content_type="application/json")
