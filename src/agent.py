import logging
import sys

from forta_agent import get_json_rpc_url, Web3, Finding, FindingSeverity, FindingType
from hexbytes import HexBytes
from src.references import *
from src.constants import *
from src.blockexplorer import *


# Initialize web3
web3 = Web3(Web3.HTTPProvider(get_json_rpc_url()))

# Replace with blockexplorer instance
blockexplorer = BlockExplorer(web3.eth.chain_id)

# Logging set up.
root = logging.getLogger()
root.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

DENOMINATOR_COUNT = 0
ALERT_COUNT = 0


def initialize():
    """
    initialize for test cases
    """
    global DENOMINATOR_COUNT
    DENOMINATOR_COUNT = 0

    global ALERT_COUNT
    ALERT_COUNT = 0


def is_contract(w3, address):
    """
    this function determines whether address is a contract
    :return: is_contract: bool
    """
    if address is None:
        return True
    code = w3.eth.get_code(Web3.toChecksumAddress(address))
    return code != HexBytes('0x')


def detect_role_change(w3, blockexplorer, transaction_event):
    """
    search transaction input when to is a contract for key words indicating a function call triggering a role change
    :return: detect_role_change: Finding
    """
    global DENOMINATOR_COUNT
    global ALERT_COUNT

    findings = []
    chain_id = w3.eth.chain_id
    network = CHAIN_LOOKUP[chain_id]
    
    if is_contract(w3, transaction_event.to):
        try:
            logging.info("Retrieving ABI from block explorer...")
            abi = blockexplorer.get_abi(transaction_event.to, network)
            logging.info("Successfully retrieved ABI from block explorer")
        except Exception:
            logging.warn("Failed to retrieve ABI from block explorer")
            return findings
        logging.info("Creating contract instance...")
        contract = w3.eth.contract(address=Web3.toChecksumAddress(transaction_event.to), abi=abi)
        logging.info("Successfully created contract instance")
        transaction = w3.eth.get_transaction(transaction_event.hash)
        transaction_data = contract.decode_function_input(transaction.input)
        logging.info(f"Decoded input: {transaction_data}")
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


def provide_handle_transaction(w3, blockexplorer):
    def handle_transaction(transaction_event):
        return detect_role_change(w3, blockexplorer, transaction_event)

    return handle_transaction


real_handle_transaction = provide_handle_transaction(web3, blockexplorer)


def handle_transaction(transaction_event):
    return real_handle_transaction(transaction_event)