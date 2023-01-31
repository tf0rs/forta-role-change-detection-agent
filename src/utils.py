import requests
import os

from src.luabase import *

def get_abi_from_luabase(address, network):

    url = "https://q.luabase.com/run"

    payload = {
        "block": {
            "data_uuid": LUABASE_CELL_UUID,
            "details": {
                "limit": 2000,
                "parameters": {
                    "network": {
                        "value": network,
                        "type": "value"
                    },
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