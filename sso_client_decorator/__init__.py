# -*-coding: utf-8 -*-
import json
import logging

import requests
import sso_client_settings as settings


def sso_request_check(request_token, auth_token):
    have_access = False
    user = None

    if not (request_token and auth_token):
        return have_access, user

    try:
        res = requests.get(settings.SSO_AUTH_TOKEN_URL, params={
            'request_token': request_token,
            'auth_token': auth_token,
            'api_key': settings.SSO_API_KEY
        }, verify=False)
        res.raise_for_status()
        response = json.loads(res.content)
        if response['success'] and response['data']['user']:
            user = {
                'id': response['data']['user'],
                'email': response['data']['email'],
            }
            have_access = True
    except Exception as e:
        logging.exception(e)

    return have_access, user


def sso_access_check(auth_token, user_id):
    have_access = False

    if not (auth_token and user_id):
        return have_access

    try:
        res = requests.get(settings.SSO_ACCESS_URL, params={
            'auth_token': auth_token,
            'user_id': int(user_id),
            'api_key': settings.SSO_API_KEY
        }, verify=False)
        res.raise_for_status()
        have_access = True
    except Exception as e:
        logging.exception(e)

    return have_access


def sso_get_request_token():
    request_token = None
    try:
        res = requests.get(settings.SSO_REQUEST_TOKEN_URL, params={
            'api_key': settings.SSO_API_KEY
        }, verify=False)
        res.raise_for_status()
        response = json.loads(res.content)
        if response['success'] and response['data']['request_token']:
            request_token = response['data']['request_token']
    except Exception as e:
        logging.exception(e)

    return request_token
