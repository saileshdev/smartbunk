from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(['POST'])
def fetch_attendance(request):
    user_name = request.data['username']
    password = request.data['password']
    return Response({"message": f'{user_name} {password}'})
