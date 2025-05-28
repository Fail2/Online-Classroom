# teacher/utils.py

import requests
from django.shortcuts import redirect

def api_request_with_refresh(request, method, url, data=None):
    access_token = request.session.get('access')
    refresh_token = request.session.get('refresh')
    headers = {'Authorization': f'Bearer {access_token}'}

    if method.lower() == 'get':
        response = requests.get(url, headers=headers)
    elif method.lower() == 'post':
        response = requests.post(url, json=data, headers=headers)
    elif method.lower() == 'put':
        response = requests.put(url, json=data, headers=headers)
    elif method.lower() == 'delete':
        response = requests.delete(url, headers=headers)
    else:
        return None

    if response.status_code == 401 and refresh_token:
        #Try to refresh the access token
        refresh_response = requests.post('http://127.0.0.1:8000/api/token/refresh/', json={'refresh': refresh_token})
        if refresh_response.status_code == 200:
            new_access = refresh_response.json().get('access')
            # Update session with new access token
            request.session['access'] = new_access
            headers['Authorization'] = f'Bearer {new_access}'

            # Retry the original request
            if method.lower() == 'get':
                return requests.get(url, headers=headers)
            elif method.lower() == 'post':
                return requests.post(url, json=data, headers=headers)
            elif method.lower() == 'put':
                return requests.put(url, json=data, headers=headers)
            elif method.lower() == 'delete':
                return requests.delete(url, headers=headers)

        else:
            return redirect('user-login')

    return response
