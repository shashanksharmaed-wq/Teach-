import json
import os
import uuid
from datetime import datetime

APPROVAL_DIR = "approvals"


def submit_for_approval(meta, plans):
    os.makedirs(APPROVAL_DIR, exist_ok=True)

    # LOCK CHECK
    for f in os.listdir(APPROVAL_DIR):
        if f.endswith(".json"):
            with open(f"{APPROVAL_DIR}/{f}", "r") as file:
                data = json.load(file)
                if data["status"] == "APPROVED" and data["meta"] == meta:
                    return None

    approval_id = str(uuid.uuid4())
    record = {
        "id": approval_id,
        "status": "PENDING",
        "submitted_at": datetime.now().isoformat(),
        "meta": meta,
        "plans": plans,
        "principal_remark": ""
    }

    with open(f"{APPROVAL_DIR}/{approval_id}.json", "w") as f:
        json.dump(record, f, indent=2)

    return approval_id


def approve_lesson(approval_id, remark=""):
    path = f"{APPROVAL_DIR}/{approval_id}.json"
    if not os.path.exists(path):
        return False

    with open(path, "r") as f:
        data = json.load(f)

    data["status"] = "APPROVED"
    data["principal_remark"] = remark
    data["approved_at"] = datetime.now().isoformat()

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return True


def is_locked(meta):
    if not os.path.exists(APPROVAL_DIR):
        return False

    for f in os.listdir(APPROVAL_DIR):
        if f.endswith(".json"):
            with open(f"{APPROVAL_DIR}/{f}", "r") as file:
                data = json.load(file)
                if data["status"] == "APPROVED" and data["meta"] == meta:
                    return True
    return False
