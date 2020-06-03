from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class LineOfCars:
    def __init__(self):
        self.change_oil_cars = []
        self.inflate_tires_cars = []
        self.diagnostic_cars = []
        self.next_ticket = 'Waiting for the next client'

    def change_oil(self, number):
        self.change_oil_cars.append(number)

    def inflate_tires(self, number):
        self.inflate_tires_cars.append(number)

    def diagnostic(self, number):
        self.diagnostic_cars.append(number)

    def work_done(self):
        self.change_oil_cars.pop(0)

    def calculate(self):
        oil = len(self.change_oil_cars)
        tires = len(self.inflate_tires_cars)
        diagnostic = len(self.diagnostic_cars)
        return [oil, tires, diagnostic]

    def processing(self):
        sum_all = sum(self.calculate())
        if sum_all == 0:
            self.next_ticket = 'Waiting for the next client'
        elif len(self.change_oil_cars) > 0:
            a = self.change_oil_cars[0]
            self.change_oil_cars.remove(self.change_oil_cars[0])
            self.next_ticket = f'Next ticket #{a}'
        elif len(self.inflate_tires_cars) > 0:
            a = self.inflate_tires_cars[0]
            self.inflate_tires_cars.remove(self.inflate_tires_cars[0])
            self.next_ticket = f'Next ticket #{a}'
        elif len(self.diagnostic_cars) > 0:
            a = self.diagnostic_cars[0]
            self.diagnostic_cars.remove(self.diagnostic_cars[0])
            self.next_ticket = f'Next ticket #{a}'
        return


line_of_cars = LineOfCars()


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        response = '<h2>Welcome to the Hypercar Service!</h2>' + \
                   f'<div>{line_of_cars.next_ticket}</div><br>' + \
                   '<div><a href="/menu">Open Menu</a></div>' + \
                   '<div><a href="/processing">Processing</a></div>'
        return HttpResponse(response)


my_links = {
    'Change oil': "/get_ticket/change_oil",
    'Inflate tires': "/get_ticket/inflate_tires",
    'Get diagnostic test': "/get_ticket/diagnostic",
    }


class MenuView3(View):
    def get(self, request, *args, **kwargs):
        response = ''
        for name, link in my_links.items():
            response += f'<div><a target="_blank" href="{link}">{name}</a></div>\n'
        return HttpResponse(response)


class MenuView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'tickets/menu.html', context={
                'links': my_links,
                }
            )


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
        return render(
            request, 'tickets/ticket.html', context={
                'number': n_car, 'time': n_minutes
                }
            )


# @require_http_methods(["GET", "POST"])
class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request, 'tickets/processing.html', context={
                'oil': len(line_of_cars.change_oil_cars),
                'tires': len(line_of_cars.inflate_tires_cars),
                'cars': len(line_of_cars.diagnostic_cars),
                }
            )

    def post(self, request, *args, **kwargs):
        line_of_cars.processing()
        # return HttpResponse(line_of_cars.processing())
        return redirect('/')
