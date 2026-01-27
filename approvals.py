import json
import os
import uuid
from datetime import datetime

APPROVAL_DIR = "approvals"


def submit_for_approval(meta, plans):
    os.makedirs(APPROVAL_DIR, exist_ok=True)

    # Check if already approved (LOCK)
    for f in os.listdir(APPROVAL_DIR):
        if f.endswith(".json"):
            with open(f"{APPROVAL_DIR}/{f}", "r", encoding="utf-8") as file:
                data = json.load(file)
                if (
                    data["status"] == "APPROVED"
                    and data["meta"]["board"] == meta["board"]
                    and data["meta"]["grade"] == meta["grade"]
                    and data["meta"]["subject"] == meta["subject"]
                    and data["meta"]["chapter"] == meta["chapter"]
                ):
                    return None  # Locked

    approval_id = str(uuid.uuid4())
    file_path = f"{APPROVAL_DIR}/{approval_id}.json"

    record = {
        "id": approval_id,
        "submitted_at": datetime.now().isoformat(),
        "status": "PENDING",
        "meta": meta,
        "plans": plans,
        "principal_remark": ""
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2)

    return approval_id


def approve_lesson(approval_id, remark=""):
    file_path = f"{APPROVAL_DIR}/{approval_id}.json"

    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["status"] = "APPROVED"
    data["principal_remark"] = remark
    data["approved_at"] = datetime.now().isoformat()

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return True


def is_locked(meta):
    if not os.path.exists(APPROVAL_DIR):
        return False

    for f in os.listdir(APPROVAL_DIR):
        if f.endswith(".json"):
            with open(f"{APPROVAL_DIR}/{f}", "r", encoding="utf-8") as file:
                data = json.load(file)
                if (
                    data["status"] == "APPROVED"
                    and data["meta"]["board"] == meta["board"]
                    and data["meta"]["grade"] == meta["grade"]
                    and data["meta"]["subject"] == meta["subject"]
                    and data["meta"]["chapter"] == meta["chapter"]
                ):
                    return True
    return False
