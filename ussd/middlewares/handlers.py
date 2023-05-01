from django.http import HttpRequest

def get_base_url(request: HttpRequest) -> str:
    scheme = request.META.get('wsgi.url_scheme', 'http')
    http_host = request.META.get('HTTP_HOST', 'localhost')
    return f"{scheme}://{http_host}"
