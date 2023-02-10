class BlockExplorerMock:

    def __init__(self, chain_id):
        pass

    def is_verified(self, address):
        if address == 'VERIFIED_CONTRACT':
            return True
        elif address == 'UNVERIFIED_CONTRACT':
            return False
        else:
            return False