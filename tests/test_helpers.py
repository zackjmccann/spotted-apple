import sys
import time
import requests
import pytest
from threading import Thread
from src.helpers import (
    create_local_http_server,
    LocalHTTPServer,
    RequestHandler,
    get_host_port
    )


@pytest.fixture
def network_location_with_colon():
    return '0.0.0.0:8080'

@pytest.fixture
def network_location_without_colon():
    return '0.0.0.0.8080'

def test_get_host_port(network_location_with_colon, network_location_without_colon):
    host_1, port_1 = get_host_port(network_location_with_colon)
    host_2, port_2 = get_host_port(network_location_without_colon)

    assert host_1 == '0.0.0.0'
    assert port_1 == 8080
    assert host_2 == network_location_without_colon
    assert port_2 is None

@pytest.fixture
def local_http_server():
    port = 8502
    return create_local_http_server(port, RequestHandler)

@pytest.fixture
def http_server_set_up(local_http_server):
    return Thread(target=local_http_server.serve_forever)

@pytest.fixture
def http_server_tear_down(local_http_server):
    return Thread(target=local_http_server.shutdown)

def test_local_server(local_http_server, http_server_set_up, http_server_tear_down):
    http_server_set_up.start()

    # Extract server details and build a request
    host, port = local_http_server.socket.getsockname()[:2]
    url_host = f'[{host}]' if ':' in host else host
    request_url = f'http://{url_host}:{port}'

    time.sleep(3) # LocalHTTPServer timeout is 10 seconds, let the server hang then send GET
    response = requests.get(request_url)
    assert response.status_code == 200
    assert response.content.decode("utf-8") == 'Connection Successful'

    # Tear down server
    http_server_tear_down.start()
