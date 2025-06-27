import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from azure.functions import HttpRequest
from functions.sessionstart import sessionstart

def test_sessionstart_success():
    payload = {
        "driverId": 45,
        "groupId": 7,
        "subGroupId": 3,
        "city": "BCN",
        "lat": 40.4168,
        "lon": -3.7038
    }
    req = HttpRequest(
        method='POST',
        url='/api/sessionstart',
        body=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )

    resp = sessionstart(req)
    assert resp.status_code == 202
    body = json.loads(resp.get_body())
    for key in payload:
        assert body[key] == payload[key]
    assert "SessionStartedAt" in body

def test_sessionstart_missing_fields():
    
    payload = {
        "driverId": 45,
        "city": "BCN"
    }
    req = HttpRequest(
        method='POST',
        url='/api/sessionstart',
        body=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    resp = sessionstart(req)
    assert resp.status_code == 422
    assert "Missing fields" in resp.get_body().decode()
