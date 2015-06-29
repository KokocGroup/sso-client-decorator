from setuptools import setup


VERSION = "0.0.1"

setup(
    name='sso-client-decorator',
    description='сlient decorator for sso authentication scheme',
    version=VERSION,
    url='https://github.com/KokocGroup/sso-client-decorator',
    download_url='https://github.com/KokocGroup/sso-client-decorator/tarball/v{}'.format(VERSION),
    packages=['sso_client_decorator'],
    install_requires=[
        'requests',
        'django'
    ],
)
