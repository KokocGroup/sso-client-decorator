# -*-coding: utf-8 -*-
import json
import logging
import urllib
from sso_client_decorator import sso_request_check, sso_access_check, sso_get_request_token
import sso_client_settings as settings
from django.http import HttpResponseRedirect

def sso_access(view):
    def call_view(*args, **kwargs):
        request = args[0]

        request_token = request.GET.get('request_token')
        auth_token_get = request.GET.get('auth_token')
        have_access, user = sso_request_check(request_token, auth_token_get)

        if not have_access:
            auth_token_cookie = request.COOKIES.get('auth_token')
            user = request.COOKIES.get('user')
            have_access = sso_access_check(auth_token_cookie, user)

        if have_access and user:
            result = view(*args, **kwargs)
            if auth_token_get:
                result.set_cookie("user", json.dumps(user), max_age=settings.SSO_COOKIES_LIVE_TIME)
                result.set_cookie("auth_token", auth_token_get, max_age=settings.SSO_COOKIES_LIVE_TIME)
        else:
            request_token = sso_get_request_token()
            redirect_to = settings.SSO_CALLBACK_URL
            if hasattr(request, 'path'):
                redirect_to += request.path
            params = {
                'request_token': request_token,
                'next': redirect_to,
                'api_key': settings.SSO_API_KEY,
            }
            redirect_url = '{}?{}'.format(
                settings.SSO_URL,
                urllib.urlencode(params),
            )

            result = HttpResponseRedirect(redirect_url)

        return result

    return call_view