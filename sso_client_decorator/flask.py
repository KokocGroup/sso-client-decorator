from __future__ import absolute_import

from functools import wraps
import urllib
from flask import abort, current_app, redirect, request
from sso_client_decorator.sso import SSOAuthentication as BaseSSOAuthentication
from werkzeug.local import LocalProxy

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class SSOAuthentication(object):

    def __init__(self, app=None):
        self.app = app
        self.sso = None
        self.config = None
        self.user_callback = None
        if self.app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.config = {
            'auth_url': app.config['SSO']['AUTH_URL'],
            'api_key': app.config['SSO']['API_KEY'],
            'callback_url': app.config['SSO']['CALLBACK_URL'],
            'request_token_url': app.config['SSO']['REQUEST_TOKEN_URL'],
            'access_url': app.config['SSO']['ACCESS_URL'],
            'auth_token_url': app.config['SSO']['AUTH_TOKEN_URL'],
            'redirect_handler': self.redirect_handler,
            'error_handler': self.error_handler
        }

        self.sso = BaseSSOAuthentication(**self.config)

        app.sso_manager = self
        app.context_processor(_user_context_processor)

    def redirect_handler(self, url):
        return redirect(url)

    def error_handler(self, status_code, msg):
        return abort(status_code)

    def user_loader(self, func):
        self.user_callback = func
        return func

    @property
    def user(self):
        return _get_user()

    def sso_access(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            request_token = request.args.get('request_token', request.cookies.get('request_token'))
            auth_token = request.args.get('auth_token', request.cookies.get('auth_token'))
            user_id = request.cookies.get('user_id')
            redirect_to = request.path
            if request.args:
                redirect_to = "{}?{}".format(redirect_to, urllib.urlencode(request.args))
            result, status = self.sso.check_authentication(request_token, auth_token, user_id, redirect_to)
            if status:
                ctx = stack.top
                if self.user_callback:
                    loaded_user = self.user_callback(result)
                    ctx.sso_user = loaded_user
                else:
                    ctx.sso_user = result
                view_result = func(*args, **kwargs)
                response = current_app.make_response(view_result)
                response.set_cookie('auth_token', auth_token)
                response.set_cookie('user_id', str(result['user']))
                response.set_cookie('request_token', request_token)
                return response
            return result
        return wrapped


def _user_context_processor():
    return dict(sso_user=_get_user())


def _get_user():
    return getattr(stack.top, 'user', None)

sso_user = LocalProxy(lambda: _get_user())
