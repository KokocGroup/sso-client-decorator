# -*-coding: utf-8 -*-
from __future__ import unicode_literals

from setuptools import setup


VERSION = "0.0.1"

setup(
    name='sso-client-decorator',
    description='client decorator for sso authentication scheme',
    version=VERSION,
    url='https://github.com/KokocGroup/sso-client-decorator',
    download_url='https://github.com/KokocGroup/sso-client-decorator/tarball/v{0}'.format(VERSION),
    packages=['sso_client_decorator'],
    install_requires=[
        'requests'
    ],
)
