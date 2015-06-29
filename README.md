sso-client
==========

Client decorator for sso authentication scheme

Need to add sso_client_settings.py file

```
from sso_client_decorator.django import sso_access

@sso_access
def view(request):
    response = TemplateResponse(request, 'index.html', {})
    return response
```
