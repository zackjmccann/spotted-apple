import pytest


def test_auth_fail_to_authenticate_service(client, bad_service_payload):
    response = client.post('/auth/authenticate/service', json=bad_service_payload)
    data = response.get_json()

    assert response.status_code == 400
    message =  data.get('message')
    assert message == 'Failed to authenticate.'

def test_auth_authenticate_service(client, good_service_payload):
    print(good_service_payload)
    response = client.post('/auth/authenticate/service', json=good_service_payload)
    data = response.get_json()

    assert response.status_code == 200
    assert data.get('access')
    assert data.get('refresh')
