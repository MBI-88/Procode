from django.http import HttpResponseBadRequest

def only_ajax(f) -> object:
    def wrapper(request:str,*args, **kwargs) -> object:
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if not is_ajax:
            return HttpResponseBadRequest()
        return f(request,*args,**kwargs)
    
    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper