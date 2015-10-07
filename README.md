sso-client
==========

Client decorator for sso authentication scheme

Install:
```
pip install sso-client-decorator
```

Need to add sso_client_settings.py file, you can copy from .default file, example:
```
cp /path/to/virtualenv_dir/.virtualenvs/virtualenv_name/src/sso-client-decorator/sso_client_decorator/sso_client_settings.default.py sso_client_settings.py
```


Uses:

```
from sso_client_decorator.sso_django import sso_access

@sso_access
def view(request):
    response = TemplateResponse(request, 'index.html', {})
    return response
```
