#! coding: utf-8

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from functools import wraps

from .utils import make_sso_client


def sso_access(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        sso = make_sso_client()
        request = args[0]
        request_token = request.GET.get('request_token')
        auth_token = request.GET.get('auth_token', request.COOKIES.get('auth_token'))
        user_id = request.COOKIES.get('user_id')
        redirect_to = request.path
        if request.GET:
            redirect_to = "{}?{}".format(redirect_to, urlencode(request.GET))
        result, status = sso.check_authentication(request_token, auth_token, user_id, redirect_to)
        if status:
            request.user = result
            response = view(*args, **kwargs)
            response.set_cookie('auth_token', auth_token)
            response.set_cookie('user_id', str(result['user']))
            return response
        return result

    return wrapped
