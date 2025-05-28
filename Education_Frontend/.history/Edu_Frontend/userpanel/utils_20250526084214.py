import requests
from django.shortcuts import redirect

def api_request_with_refresh(request,method,url,data = None):
    access_token = request.session.get('access')
    refresh_token = request.session.get('refresh')
    