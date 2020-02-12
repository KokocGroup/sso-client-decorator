# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = "0.0.19"

setup(
    name='sso-client-decorator',
    description='client decorator for sso authentication scheme',
    version=VERSION,
    url='https://github.com/KokocGroup/sso-client-decorator',
    download_url='https://github.com/KokocGroup/sso-client-decorator/tarball/v{0}'.format(VERSION),
    packages=find_packages(),
    package_dir={'sso_client_decorator': 'sso_client_decorator'},
    install_requires=[
        'requests'
    ],
)
