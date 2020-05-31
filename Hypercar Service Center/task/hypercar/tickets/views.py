from django.http.response import HttpResponse
from django.views import View


class LineOfCars:
    def __init__(self):
        self.change_oil_cars = []
        self.inflate_tires_cars = []
        self.diagnostic_cars = []

    def change_oil(self, number):
        self.change_oil_cars.append(number)

    def inflate_tires(self, number):
        self.inflate_tires_cars.append(number)

    def diagnostic(self, number):
        self.diagnostic_cars.append(number)

    def calculate(self):
        oil = len(self.change_oil_cars)
        tires = len(self.inflate_tires_cars)
        diagnostic = len(self.diagnostic_cars)
        return [oil, tires, diagnostic]


line_of_cars = LineOfCars()


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2><div><a href="/menu">Open Menu</a></div>')


my_links = {
    'Change oil': "/get_ticket/change_oil",
    'Inflate tires': "/get_ticket/inflate_tires",
    'Get diagnostic test': "/get_ticket/diagnostic",
    }


class MenuView(View):
    def get(self, request, *args, **kwargs):
        response = ''
        for name, link in my_links.items():
            response += f'<div><a target="_blank" href="{link}">{name}</a></div>\n'
        return HttpResponse(response)


class TicketView(View):

    def get(self, request, service, *args, **kwargs):
        car_list = line_of_cars.calculate()
        n_car = sum(car_list) + 1
        if service == 'change_oil':
            n_minutes = car_list[0] * 2
        elif service == 'inflate_tires':
            n_minutes = car_list[0] * 2 + car_list[1] * 5
        else:
            n_minutes = car_list[0] * 2 + car_list[1] * 5 + car_list[2] * 30
        eval(f"line_of_cars.{service}({n_car})")
        response = f'<div>Your number is {n_car}</div>\n<div>Please wait around {n_minutes} minutes'
        return HttpResponse(response)
