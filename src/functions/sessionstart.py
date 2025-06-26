import logging
import json
from datetime import datetime,timezone
import azure.functions as func



REQUIRED_FIELDS = {"driverId", "groupId", "subGroupId", "city", "lat", "lon"}

def sessionstart(req: func.HttpRequest) -> func.HttpResponse:
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

    return func.HttpResponse(
        json.dumps(body), mimetype="application/json", status_code=202
    )
