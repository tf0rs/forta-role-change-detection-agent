import agent
from forta_agent import FindingSeverity, create_transaction_event
from src.web3_mock import Web3Mock, NEW_EOA, OLD_EOA, NEW_CONTRACT

w3 = Web3Mock()

class TestChangeNowFundingAgent:

    def test_transfer_to_contract(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': NEW_CONTRACT,
                'from': "0x077d360f11d220e4d5d831430c81c26c9be7c4a4",
                'value': "1000000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_changenow_funding(w3, tx_event)
        assert len(findings) == 0, "This should have not triggered a finding as the to is a contract"


    def test_not_transfer_from_changenow(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': NEW_EOA,
                'from': OLD_EOA,
                'value': "1000000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_changenow_funding(w3, tx_event)
        assert len(findings) == 0, "This should have not triggered a finding as the from is not Changenow"


    def test_transfer_from_changenow_to_new_account(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': NEW_EOA,
                'from': "0x077d360f11d220e4d5d831430c81c26c9be7c4a4",
                'value': "100000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_changenow_funding(w3, tx_event)
        assert len(findings) == 1, "This should have triggered a finding"
        assert findings[0].alert_id == "FUNDING-CHANGENOW-NEW-ACCOUNT", "This is a tx from Changenow to a new account"
        assert findings[0].severity == FindingSeverity.Low, "Severity should be low"


    def test_low_value_transfer_from_changenow(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'hash': "0",
                'to': OLD_EOA,
                'from': "0x077d360f11d220e4d5d831430c81c26c9be7c4a4",
                'value': "300000000000000000"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_changenow_funding(w3, tx_event)
        assert len(findings) == 1, "This should have triggered a finding"
        assert findings[0].alert_id == "FUNDING-CHANGENOW-LOW-AMOUNT", "This is a high value transfer from Changenow"
        assert findings[0].severity == FindingSeverity.Low, "Severity should be low"
