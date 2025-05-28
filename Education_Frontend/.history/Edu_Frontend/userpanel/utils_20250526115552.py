# utils.py
import requests
from django.shortcuts import redirect

def api_request_with_refresh(request, method, url, data=None,files = None):
    """
    ✅ Handles API requests with JWT access + refresh token logic.
    ✅ Automatically refreshes token if access token is expired.
    ✅ Returns API response or redirects to login if failed.
    """
    access_token = request.session.get('access')
    refresh_token = request.session.get('refresh')
    headers = {'Authorization': f'Bearer {access_token}'}

    try:
        # Choose method dynamically
        method_func = getattr(requests, method.lower())
        # getattr(requests, method.lower()) this return requests.post (example)
        response = method_func(url, headers=headers, json=data, files = files)
    except Exception as e:
        return None  # Optional: Handle logging

    # If access token is expired
    if response.status_code == 401 and refresh_token:
        refresh_response = requests.post(
            'http://127.0.0.1:8000/api/token/refresh/',
            json={'refresh': refresh_token}
        )
        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            request.session['access'] = new_tokens['access']
            headers = {'Authorization': f'Bearer {new_tokens["access"]}'}
            response = method_func(url, headers=headers, json=data,files = files)
        else:
            return redirect('user-login')

    return response
