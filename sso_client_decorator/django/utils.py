from django.conf import settings
from sso_client_decorator.sso import SSOAuthentication
from django.http import HttpResponseRedirect, HttpResponse


def make_sso_client():
    return SSOAuthentication(
        auth_url=settings.SSO['AUTH_URL'],
        api_key=settings.SSO['API_KEY'],
        callback_url=settings.SSO['CALLBACK_URL'],
        request_token_url=settings.SSO['REQUEST_TOKEN_URL'],
        access_url=settings.SSO['ACCESS_URL'],
        auth_token_url=settings.SSO['AUTH_TOKEN_URL'],
        redirect_handler=redirect_handler,
        error_handler=error_handler
    )


def redirect_handler(url):
    return HttpResponseRedirect(url)


def error_handler(status_code, msg):
    return HttpResponse(status_code, msg)
