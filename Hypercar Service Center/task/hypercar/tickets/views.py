from django.http.response import HttpResponse
from django.views import View

my_links = {'Change oil'         : "/get_ticket/change_oil", 'Inflate tires': "/get_ticket/inflate_tires",
            'Get diagnostic test': "/get_ticket/diagnostic", }


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    def get(self, request, *args, **kwargs):
        response = ''
        for name, link in my_links.items():
            response += f'<a target="_blank" href="{link}">{name}</a><br>'
        return HttpResponse(response)
