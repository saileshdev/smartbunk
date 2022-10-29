from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


@api_view(['POST'])
def fetch_attendance(request):

    user_name = request.data.get('username')
    if user_name is None:
        error = "Please send a valid username"
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    password = request.data.get('password')
    if password is None:
        error = "Please send a valid password"
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'success': 'True'})
