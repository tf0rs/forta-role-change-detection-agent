import logging
import sys

from forta_agent import get_json_rpc_url, Web3, Finding, FindingSeverity, FindingType
from hexbytes import HexBytes
from src.luabase import *
from src.constants import *
from src.utils import *


#Initialize web3.
web3 = Web3(Web3.HTTPProvider(get_json_rpc_url()))

# Logging set up.
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def initialize():
    """
    initialize for test cases
    """


def is_contract(w3, address):
    """
    this function determines whether address is a contract
    :return: is_contract: bool
    """
    if address is None:
        return True
    code = w3.eth.get_code(Web3.toChecksumAddress(address))
    return code != HexBytes('0x')


def detect_role_change(w3, transaction_event):
    """
    search transaction input when to is a contract for key words indicating a function call triggering a role change
    :return: detect_role_change: Finding
    """
    findings = []
    chain_id = w3.eth.chain_id
    network = CHAIN_LOOKUP[chain_id]
    
    if is_contract(w3, transaction_event.to):
        """
        Need to implement some error handling here for situations where Luabase doesn't have the abi.
        """
        try:
            abi = get_abi_from_luabase(transaction_event.to, network)
        except Exception as e:
            logging.info(f"Invalid response from Luabase: {e}")
            return findings
        contract = w3.eth.contract(address=Web3.toChecksumAddress(transaction_event.to), abi=abi)
        transaction = w3.eth.get_transaction(transaction_event.hash)
        transaction_data = contract.decode_function_input(transaction.input)
        matching_keywords = []
        for keyword in ROLE_CHANGE_KEYWORDS:
            if keyword in str(transaction_data).lower():
                matching_keywords.append(keyword)
        if len(matching_keywords) > 0:
            findings.append(Finding(
                {
                    "name": "Possible Role Change",
                    "description": f"Possible role change affecting {transaction_event.transaction.to}",
                    "alert_id": "ROLE-CHANGE-1",
                    "type": FindingType.Suspicious,
                    "severity": FindingSeverity.Low,
                    "metadata": {
                        "matching keywords": matching_keywords,
                        "function signature": str(transaction_data[0])[10:-1]
                    }
                }
            ))

    return findings


def provide_handle_transaction(w3):
    def handle_transaction(transaction_event):
        return detect_role_change(w3, transaction_event)

    return handle_transaction


real_handle_transaction = provide_handle_transaction(web3)


def handle_transaction(transaction_event):
    return real_handle_transaction(transaction_event)