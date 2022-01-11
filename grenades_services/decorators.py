"""
Decorators
"""


from django.http import HttpResponseRedirect, HttpResponse


def iamdecorator(function_obj):
    """
    iamdecorator
    This 'iamdecorator' function used to call http login required decorator
    """
    def wrap(request, *args, **kwargs):
        """
        wrap decorator function
        """
        print(request)
        print(request.user.id)
        if request.user.id:
            print("i will redirect ")
            return HttpResponseRedirect("/")
        else:
            return function_obj(request, *args, **kwargs)
        return function_obj(request, *args, **kwargs)
    return wrap
