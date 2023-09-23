from django.shortcuts import render
from django.views.generic import View
import rsa

def sign(message, key):
    return str(rsa.sign(message.encode(), key, 'SHA-1'))

def verify(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key,) == 'SHA-1'
    except:
        return False


class Viewer(View):
    form_class = object
    template_name = None
    context = dict()

    def __init__(self, **kwargs) -> None:
        self.context['form'] = self.form_class()
        super().__init__(**kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.get_template_name(), self.get_context())

    def post(self, request):
        self.form = request.POST
        self.form_valid()
        return render(request, self.get_template_name(), self.get_context())

    def form_valid(self):
        return render(self.request, self.get_template_name(), self.get_context())

    def get_context(self):
        return self.context

    def get_template_name(self):
        return self.template_name