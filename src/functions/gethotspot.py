import json
import logging
import os
from datetime import datetime
from typing import Optional

import azure.functions as func
from azure.storage.blob import BlobClient, BlobServiceClient

STORAGE_CONN        = os.environ["BLOB_CONN"]
CONTAINER           = os.environ["CONTAINER"]
PREFIX_HOTSPOT_BLOB = os.environ["PREFIX_HOTSPOT_BLOB"]

blob_service      = BlobServiceClient.from_connection_string(STORAGE_CONN)
container_client  = blob_service.get_container_client(CONTAINER)

def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def _blob_json(blob_name: str) -> Optional[dict]:
    """Return JSON from blob or {} (on failure)."""
    try:
        blob: BlobClient = blob_service.get_blob_client(CONTAINER, blob_name)
        return json.loads(blob.download_blob().readall())
    except Exception as exc:
        logging.warning("Blob %s not available (%s)", blob_name, exc)
        return {}

def _latest_hotspot() -> Optional[dict]:
    latest      = None
    latest_ts   = None

    for blob in container_client.list_blobs(name_starts_with=PREFIX_HOTSPOT_BLOB):
        if not blob.name.endswith(".json"):
            continue

        hotspot = _blob_json(blob.name)
        if not hotspot or "lastUpdated" not in hotspot:
            continue

        try:
            ts = _parse_ts(hotspot["lastUpdated"])
        except Exception:
            continue

        if latest is None or ts > latest_ts:
            latest, latest_ts = hotspot, ts

    return latest

def get_hotspot(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("get_hotspot invoked")

    group_id = req.params.get("groupId")
    if group_id:
        blob_path = f"{PREFIX_HOTSPOT_BLOB}/hotspot-{group_id}.json"
        hotspot   = _blob_json(blob_path)
        if hotspot:
            return func.HttpResponse(json.dumps(hotspot), mimetype="application/json")
        return func.HttpResponse(
            f"Hotspot for group '{group_id}' not found",
            status_code=404
        )

    hotspot = _latest_hotspot()
    if hotspot:
        return func.HttpResponse(json.dumps(hotspot), mimetype="application/json")
    return func.HttpResponse("No hotspots found", status_code=404)