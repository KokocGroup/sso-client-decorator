sso-client
==========

Client decorator for sso authentication scheme

Install:
```
pip install sso-client-decorator
```

Uses:

```
from sso_client_decorator.sso_django import sso_access

@sso_access
def view(request):
    response = TemplateResponse(request, 'index.html', {})
    return response
```


