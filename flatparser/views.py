from django.shortcuts import render
from rest_framework import views, response


class ApiParser(views.APIView):

    def get(self, request, format=None):
        return response.Response(status=200, data={ 'response': 'OK' })
