from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))


class Station:
    def __init__(self, name, street, district):
        self.Name = name
        self.Street = street
        self.District = district


class Page:
    def __init__(self, number, all_pages):
        self.number = number
        self.all_pages = all_pages
        if self.number != 1:
            self.has_previous = True
            self.previous_page_number = self.number - 1
        if self.number < self.all_pages:
            self.has_next = True
            self.next_page_number = number + 1


def bus_stations(request):
    page_number = int(request.GET.get('page', 1))
    element_per_page = 10
    context = {
        'bus_stations': "",
        'page': 0,
    }
    all_bus_stations = []

    file = settings.BUS_STATION_CSV
    with open(file, "r", encoding="utf-8") as file:
        for symbol in file.read():
            if symbol == "\n":
                context['page'] += 1
        file.seek(0)
        for _ in range(context["page"]):
            line = file.readline()
            line = line.split(",")
            if len(line) < 17:
                continue
            station = Station(f"{line[1]} {line[2]}", f"{line[5]}", f"{line[7]}")
            all_bus_stations.append(station)

    paginator = Paginator(all_bus_stations, element_per_page)
    page = paginator.get_page(page_number)
    current_page = Page(page_number, paginator.num_pages)
    context["page"] = current_page
    context["bus_stations"] = page

    return render(request, 'stations/index.html', context)
