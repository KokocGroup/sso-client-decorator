import json
import logging
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import requests


class SSOAuthentication(object):

    def __init__(self, auth_url, api_key, callback_url, request_token_url, access_url, auth_token_url, error_handler, redirect_handler):
        self.api_key = api_key
        self.auth_url = auth_url
        self.callback_url = callback_url
        self.request_token_url = request_token_url
        self.access_url = access_url
        self.auth_token_url = auth_token_url
        self.redirect_handler = redirect_handler
        self.error_handler = error_handler

    def request_check(self, request_token, auth_token):
        have_access = False
        user = None
        if not (request_token and auth_token):
            return have_access, user

        try:
            res = requests.get(self.auth_token_url, params={
                'request_token': request_token,
                'auth_token': auth_token,
                'api_key': self.api_key
            }, verify=False)

            res.raise_for_status()
            response = json.loads(res.content.decode('utf-8'))
            if response['success'] and response['data']['user']:
                user = response['data']
                have_access = True
        except requests.HTTPError as e:
            if e.response.status_code >= 500:
                logging.exception(e)
        except Exception as e:
            logging.exception(e)

        return have_access, user

    def check_authentication(self, request_token=None, auth_token=None, user_id=None, redirect_next=None):
        have_access, user = self.request_check(request_token, auth_token)
        if not have_access:
            have_access, user = self.access_check(auth_token, user_id)

        if have_access and user:
            return user, True
        else:
            request_token = self.get_token()
            if not request_token:
                return self.error_handler(403, 'Forbidden, cause SSO server is not responding'), False

            params = {
                'request_token': request_token,
                'next': self.callback_url + redirect_next or '',
                'api_key': self.api_key,
            }
            redirect_url = '{0}?{1}'.format(
                self.auth_url,
                urlencode(params),
            )

            result = self.redirect_handler(redirect_url)

        return result, False

    def access_check(self, auth_token, user_id):
        have_access = False
        user = None
        if not (auth_token and user_id):
            return have_access, user

        try:
            res = requests.get(self.access_url, params={
                'auth_token': auth_token,
                'user_id': int(user_id),
                'api_key': self.api_key
            }, verify=False)
            res.raise_for_status()
            response = json.loads(res.content.decode('utf-8'))
            if response['success'] and response['data']['user']:
                user = response['data']
                have_access = True
        except requests.HTTPError as e:
            if e.response.status_code >= 500:
                logging.exception(e)
        except Exception as e:
            logging.exception(e)

        return have_access, user

    def get_token(self):
        request_token = None
        try:
            res = requests.get(self.request_token_url, params={
                'api_key': self.api_key
            }, verify=False)
            res.raise_for_status()
            response = json.loads(res.content.decode('utf-8'))
            if response['success'] and response['data']['request_token']:
                request_token = response['data']['request_token']
        except Exception as e:
            logging.exception(e)
        return request_token
