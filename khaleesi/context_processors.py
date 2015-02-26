from khaleesi.settings import URL_HOST

def context_url_host(request):
    return {'URL_HOST': URL_HOST}
