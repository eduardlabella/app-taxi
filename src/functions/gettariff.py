import json
import logging
import os
from datetime import datetime, timezone

import azure.functions as func
from azure.storage.blob import BlobClient, BlobServiceClient

STORAGE_CONN = os.environ["BLOB_CONN"]
CONTAINER    = os.environ["CONTAINER"]
PREFIX_TARIFF_BLOB  = os.environ["PREFIX_TARIFF_BLOB"]

blob_service = BlobServiceClient.from_connection_string(STORAGE_CONN)


def _blob_json(path: str) -> dict:
    """Return JSON from blob or {}."""
    try:
        blob: BlobClient = blob_service.get_blob_client(CONTAINER, path)
        return json.loads(blob.download_blob().readall())
    except Exception as exc:
        logging.warning("Blob %s not available (%s)", path, exc)
        return {}

def _default_group_by_hour(hour: int) -> str:
    """Return tariff group based on hour UTC."""
    return "g2" if hour >= 22 or hour < 6 else "g1"

# EntryPoint
def get_tariff(req: func.HttpRequest) -> func.HttpResponse:
    """
    GET /external/v1/tariff          -> auto-select by time of day
    GET /external/v1/tariff?groupId=g2  -> force specific group
    """
    logging.info("get_tariff invoked")

    group_id = (req.params.get("groupId") or
                _default_group_by_hour(datetime.now(timezone.utc).hour))
    
    blob_path = f"{PREFIX_TARIFF_BLOB}/group-{group_id}.json"

    tariff_json = _blob_json(blob_path)
    if not tariff_json:
        return func.HttpResponse(
            f"Tariff for group '{group_id}' not found", status_code=404
        )

    return func.HttpResponse(
        json.dumps(tariff_json),
        mimetype="application/json",
        status_code=200
    )
