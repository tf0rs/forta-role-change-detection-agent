import requests
import os


LUABASE_API_KEY = "placeholder"
LUABASE_CELL_UUID = "dc8331accdf54eed9321958b1e805f76"


def get_abi_from_luabase(address):

    url = "https://q.luabase.com/run"

    payload = {
        "block": {
            "data_uuid": LUABASE_CELL_UUID,
            "details": {
                "limit": 2000,
                "parameters": {
                    "screened_address": {
                        "type": "value",
                        "value": f"'{str.lower(address)}'"
                    }
                }
            }
        },
        "api_key": LUABASE_API_KEY,
    }
    headers = {"content-type": "application/json"}
    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.json()

    abi = data['data'][0]['abi']

    return abi