import agent
from forta_agent import create_transaction_event
from src.web3_mock import *
from src.blockexplorer_mock import BlockExplorerMock

w3 = Web3Mock()
blockexplorer = BlockExplorerMock(w3.eth.chain_id)

class TestRoleChangeAgent:

    def test_transfer_with_role_change(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'to': VERIFIED_CONTRACT,
                'from': NEW_EOA,
                'hash': "0x30a332902920cb6886281f6d28abfa5775559647eb7288e7cc00763fe4427f7b"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_role_change(w3, blockexplorer, tx_event)
        assert len(findings) == 1, "This should have triggered a finding as there is a role change"


    def test_transfer_without_role_change(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'to': VERIFIED_CONTRACT,
                'from': NEW_EOA,
                'hash': "0x8fc91a50a2614d323864655c2473ec19e58cb356a9f1d391888c472476c749f7"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_role_change(w3, blockexplorer, tx_event)
        assert len(findings) == 0, "This should not have triggered a finding - no role change"

    
    def test_transfer_to_eoa(self):
        agent.initialize()

        tx_event = create_transaction_event({
            'transaction': {
                'to': NEW_EOA,
                'from': OLD_EOA,
                'hash': "0x8fc91a50a2614d323864655c2473ec19e58cb356a9f1d391888c472476c749f7"
            },
            'block': {
                'number': 1
            },
            'receipt': {
                'logs': []
            }
        })

        findings = agent.detect_role_change(w3, blockexplorer, tx_event)
        assert len(findings) == 0, "This should not have triggered a finding - not to a contract"
