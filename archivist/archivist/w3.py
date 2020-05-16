from typing import List


from eth_utils.hexadecimal import decode_hex
from web3 import Web3

from archivist.types import Transaction

# TODO: don't expose this
INFURA_URL = 'https://mainnet.infura.io/v3/94cc5e7210024cbda2686a62ae4e267a'

# NOTE: just for testing!
POAP_CONTRACT_BLOCK = 7228178


class W3():
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(INFURA_URL))

    def latest_block(self) -> int:
        w3_response = self.w3.eth.getBlock('latest')
        return w3_response.number

    # NOTE: block is str or int type. i.e. 'latest' or a number
    def block_to_txes(self, block) -> List[Transaction]:
        resp = self.w3.eth.getBlock(block, True)
        return [Transaction(resp_tx['blockNumber'],
                            resp_tx['hash'].hex(),
                            resp_tx['from'],
                            resp_tx['to'],
                            resp_tx['nonce'],
                            decode_hex(resp_tx['input']))
                for resp_tx in resp['transactions']]
