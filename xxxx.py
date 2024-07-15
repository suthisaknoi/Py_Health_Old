import requests
import json


def post_authen():
    url = 'http://localhost:8189/api/nhso-service/confirm-save'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': 'Bearer d3b7763e-a3ac-4b16-885b-0d4345995ee5'
    }
    payload = {
        "pid": "3650600299197",
        "claimType": "PG0120001",
        "mobile": "0901975166",
        "correlationId": "1961eaf8-0c7f-4cdb-b3e4-e831e45694dc",
        "hn": "99",
        "hcode": "11272"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            print('Request was successful.')
            response_data = response.json()
            pid = response_data.get('pid')
            claimType = response_data.get('claimType')
            correlationId = response_data.get('correlationId')
            createdDate = response_data.get('createdDate')
            claimCode = response_data.get('claimCode')
            print(
                f'pid: {pid}, claimType: {claimType}, correlationId: {correlationId}, createdDate: {createdDate}, claimCode: {claimCode}')
        elif response.status_code == 400:
            print('Bad Request:', response.json())
        elif response.status_code == 404:
            print('The requested resource could not be found.')
        else:
            print('Error:', response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        print('Error:', e)


# Call the function
post_authen()
