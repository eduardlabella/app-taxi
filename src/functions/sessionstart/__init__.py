import json
import logging
import os
from datetime import datetime, timezone

import azure.functions as func
import requests

GETTARIFF_URL  = os.environ["GETTARIFF_URL"]
GETHOTSPOT_URL  = os.environ["GETHOTSPOT_URL"]
REQUIRED_FIELDS = {"driverId", "groupIdTariff", "groupIdHotspot", "city", "lat", "lon"}

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("sessionstart invoked")

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    missing = REQUIRED_FIELDS - body.keys()
    if missing:
        return func.HttpResponse(
            f"Missing fields: {', '.join(sorted(missing))}",
            status_code=422,
        )

    body["SessionStartedAt"] = datetime.now(timezone.utc).isoformat()

    # GETTARIFF
    try:
        response = requests.get(
            GETTARIFF_URL,
            params={"groupId": body["groupIdTariff"]},
            timeout=10,
        )
        response.raise_for_status()
        tariff_result = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling gettariff: {e}")
        return func.HttpResponse(f"Error calling gettariff: {e}", status_code=500)
    
    if not body.get("groupIdTariff"):
        if "groupId" in tariff_result:
            body["groupIdTariff"] = tariff_result["groupId"]
    

    # GET HOTSPOT
    try:
        response = requests.get(
            GETHOTSPOT_URL,
            params={"groupId": body["groupIdHotspot"]},
            timeout=10,
        )
        response.raise_for_status()
        hotspot_result = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling gethotspot: {e}")
        return func.HttpResponse(f"Error calling gethotspot: {e}", status_code=500)    

    if not body.get("groupIdHotspot"):
        if "groupId" in hotspot_result:
            body["groupIdHotspot"] = hotspot_result["groupId"]

    response_data = {
        "session": body,
        "hotspot": hotspot_result,
        "tariff": tariff_result
    }

    return func.HttpResponse(
        json.dumps(response_data),
        mimetype="application/json",
        status_code=202,
    )
