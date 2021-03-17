from functools import wraps
import os
import jwt
from django.http import HttpResponse
from .utils import *
import json
import logging

logger = logging.getLogger(__name__)


def login_required_and_get_request_parameter(f):
    @wraps(f)
    def token_validator(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        kwargs['page'] = request.GET.get('page', 1)
        kwargs['limit'] = request.GET.get('limit', 10)
        kwargs['id'] = request.GET.get('id')
        logger.error('token is: {token}'.format(token=token))
        if not token:
            return HttpResponse(json.dumps(HttpErrorHandler.bad_request_error()), content_type="application/json")
        try:
            kwargs['user_data'] = jwt.decode(token.split()[1], os.environ.get("JWT_SECRET_KEY", "xyz"), algorithms="HS256")
            logger.error('User Data  is: {data}'.format(data=kwargs['user_data']))
        except:
            logger.error('JWT Token Exception ')
            return HttpResponse(json.dumps(HttpErrorHandler.invalid_token()), content_type="application/json")
        return f(*args, **kwargs)

    return token_validator

