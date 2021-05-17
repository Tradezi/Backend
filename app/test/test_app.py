import math
import requests

def test_current_api():
    r = requests.get("http://localhost:5008/api/stocks/current?symbol=aapl")
    data = r.json()
    assert sorted(data) == sorted(['price', 'company', 'symbol'])


def test_history_api():
    r = requests.get("http://localhost:5008/api/stocks/history?symbol=aapl&years=1")
    data = r.json()
    assert type(data).__name__ == 'list'
    assert sorted(data[0]) == sorted(['date', 'close', 'open', 'high', 'low'])

def test_auth():
    r = requests.get("http://localhost:5008/api/user/details")
    data = r.json()
    assert data['error'] == 'Authentication token is not available, please login to get one'