def test_get_host_port():
    from src.helpers import get_host_port
    network_location_1 = 'localhost:8080'
    network_location_2 = '0.0.0.0:8080'
    network_location_3 = '0.8.0.8.8500'

    host_1, port_1 = get_host_port(network_location_1)
    host_2, port_2 = get_host_port(network_location_2)
    host_3, port_3 = get_host_port(network_location_3)

    assert host_1 == 'localhost'
    assert port_1 == 8080
    assert host_2 == '0.0.0.0'
    assert port_2 == 8080
    assert host_3 == network_location_3
    assert port_3 is None

def test_local_server():
    """
    The testing of the local HTTP server and server creation and (request handler)
    is all administered via this test case due to their close coupling.
    """
    import sys
    import time
    import requests
    from threading import Thread
    from src.helpers import create_local_http_server, LocalHTTPServer, RequestHandler

    port = 8502
    local_server = create_local_http_server(port, RequestHandler)

    # Start HTTP server in a thread
    httpthread = Thread(target=local_server.serve_forever)
    httpthread.start()

    # Extract detail and build a request
    host, port = local_server.socket.getsockname()[:2]
    url_host = f'[{host}]' if ':' in host else host
    request_url = f'http://{url_host}:{port}'

    # LocalHTTPServer timeout is 10 seconds, let the server hang then send GET
    time.sleep(3)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(request_url, headers=headers)
    assert response.status_code == 200
    assert response.content.decode("utf-8") == 'Connection Successful'

    # Tear down server from another thread
    killerthread = Thread(target=local_server.shutdown)
    killerthread.start()
