from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SBUser, Payment, APIUsage

# Create your views here.


def scrape_data(sb_user):

    # Make scrape api call here

    try:
        api_usage = APIUsage.objects.get(user=sb_user)
        api_usage.count = api_usage.count + 1
        api_usage.save()
    except APIUsage.DoesNotExist:
        api_usage = APIUsage(user=sb_user, api_name="fetchAttendance", count=0)
        api_usage.save()
    return 'This is a sample scraped data'


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

    try:
        sb_user = SBUser.objects.get(user_name=user_name)
        try:
            payment_status = Payment.objects.get(user=sb_user)
        except Payment.DoesNotExist:
            return Response({'message': 'The user needs to pay to continue'})

        if payment_status is False:
            return Response({'message': 'The user needs to pay to continue'})

        message = scrape_data(sb_user)
        return Response({'message': message})

    except SBUser.DoesNotExist:
        sb_user = SBUser(user_name=user_name)
        sb_user.save()
        message = scrape_data(sb_user)
        return Response({'message': message})
