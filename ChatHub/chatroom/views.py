from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

def index(request):
    return render(request, "index.html")

@login_required
def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})