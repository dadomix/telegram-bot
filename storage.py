import json
import os

FILE = "keys.json"

def load_keys():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_keys(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ✅ ADD KEY (FIXED)
def add_key(panel, days, key):
    data = load_keys()

    if panel not in data:
        data[panel] = {}

    if days not in data[panel]:
        data[panel][days] = []

    data[panel][days].append(key)

    save_keys(data)

# ✅ GET KEY (ALSO IMPORTANT)
def get_key(panel, days):
    data = load_keys()

    if panel not in data:
        return None

    if days not in data[panel]:
        return None

    if not data[panel][days]:
        return None

    key = data[panel][days].pop(0)  # remove first key

    save_keys(data)
    return key