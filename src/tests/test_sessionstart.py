import json
import os
import re
import sys
from unittest.mock import MagicMock, patch

from azure.functions import HttpRequest

os.environ["GETTARIFF_URL"]  = "http://mock/gettariff"
os.environ["GETHOTSPOT_URL"] = "http://mock/gethotspot"


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.sessionstart import sessionstart

ISO_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?[+-]\d{2}:\d{2}$"
)

def _mock_response(payload: dict) -> MagicMock:
    """Return a MagicMock that mimics requests.Response."""
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = payload
    return mock_resp


@patch("functions.sessionstart.requests.get")
def test_sessionstart_response_shape(mock_get):
    """Verify that the response matches the expected JSON shape (timestamp is validated by format only)."""

    tariff_json = {
        "groupId": "g1",
        "version": 18,
        "description": "Urban day rate",
        "baseFare": 2.5,
        "kmRate": 1.1,
        "minimumFare": 4.0,
        "currency": "EUR",
        "validFrom": "2025-06-25T00:00:00Z",
        "updatedAt": "2025-06-25T07:45:00Z",
    }
    hotspot_json = {
        "groupId": "g3",
        "lat": 41.3810,
        "lon": 2.1905,
        "nearestHotspot": "Forum",
        "distanceMeters": 410,
        "lastUpdated": "2025-06-28T07:59:10Z",
    }

    def side_effect(url, *args, **kwargs):
        if "gettariff" in url:
            return _mock_response(tariff_json)
        if "gethotspot" in url:
            return _mock_response(hotspot_json)
        raise ValueError(f"Unexpected URL in test: {url}")

    mock_get.side_effect = side_effect

    # --- Call sessionstart ---
    incoming_payload = {
        "driverId": 45,
        "groupIdTariff": "g1",
        "groupIdHotspot": "g3",
        "city": "BCN",
        "lat": 40.4168,
        "lon": -3.7038,
    }
    req = HttpRequest(
        method="POST",
        url="/api/sessionstart",
        body=json.dumps(incoming_payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    resp = sessionstart(req)
    assert resp.status_code == 202

    result = json.loads(resp.get_body())

    # --- Basic shape checks ---
    assert set(result) == {"session", "tariff", "hotspot"}

    # 1. Session
    session_block = result["session"]
    for k in incoming_payload:
        assert session_block[k] == incoming_payload[k]
    assert "SessionStartedAt" in session_block and ISO_REGEX.match(session_block["SessionStartedAt"])

    # 2. Tariff & Hotspot
    assert result["tariff"] == tariff_json
    assert result["hotspot"] == hotspot_json