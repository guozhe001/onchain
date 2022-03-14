from django.shortcuts import render
from schedule import schedule

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the hunter index.\n")


print("hello views")
schedule.start()

