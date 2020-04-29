import rlp
import sqlite3

from eth_hash.auto import keccak
from eth_utils.conversions import to_hex
from eth_utils.hexadecimal import decode_hex
from web3 import Web3

# TODO: don't expose in git
INFURA_URL = 'https://mainnet.infura.io/v3/94cc5e7210024cbda2686a62ae4e267a'
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/94cc5e7210024cbda2686a62ae4e267a'))


# NOTE: change based on mount location of volume
DB_LOCATION = 'data.db'


def init_db():
    db = sqlite3.connect(DB_LOCATION)
    c = db.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS contract_bytecode (block integer, address text, bytecode text)')
    c.execute('CREATE TABLE IF NOT EXISTS latest_block (block integer)')

    db.commit()

    return db


db = init_db()


def latest_db_block():
    c = db.cursor()
    blocks = list(c.execute('SELECT block FROM latest_block ORDER BY block DESC LIMIT 1'))

    if len(blocks) == 0:
        return 0
    else:
        return blocks[0][0]


def add_latest_block(b):
    c = db.cursor()
    c.execute(f'INSERT INTO latest_block (block) VALUES ({b})')
    db.commit()
    return b


def add_contract_bytecode(block: int, address: str, bytecode: str):
    c = db.cursor()
    c.execute(
        f'INSERT INTO contract_bytecode (block, address, bytecode) VALUES ({block},{address},{bytecode})')
    db.commit()
    return (block, address, bytecode)


# NOTE: just for testing
def reset_latest_block():
    c = db.cursor()
    c.execute('DELETE FROM latest_block')
    db.commit()


# NOTE: if I want to add additional fields to sql table, this is where I'd do it
def write_contract_tx_bytecode(tx):
    contract_address = generate_contract_address(tx['from'], tx['nonce'])

    # NOTE: I may opt to pull out the *actual* contract bytecode from this in the future
    contract_bytecode = tx['input']
    block = tx['blockNumber']

    add_contract_bytecode(block, contract_address, contract_bytecode)


def generate_contract_address(from_address: str, nonce: int):
    rlp_encoded = rlp.encode([decode_hex(from_address), nonce])
    hashed = keccak(rlp_encoded)

    return force_bytes_to_address(hashed)


def force_bytes_to_address(value: bytes):
    trimmed_value = value[-20:]
    padded_value = trimmed_value.rjust(20, b'\x00')

    return to_hex(padded_value)


REORG_BUFFER = 20


def latest_web3_block():
    # NOTE: take actual latest - N, to provide re-org protection
    web3_response = w3.eth.getBlock('latest')
    return web3_response.number - 20


# NOTE: may want to verify that this is all we need, i.e. that we don't need 0x0 checks
def is_contract_tx(tx):
    return tx['to'] is None


def get_block_contract_txes(block):
    block = w3.eth.getBlock(block, True)
    contract_txes = [tx for tx in block['transactions'] if is_contract_tx(tx)]

    return contract_txes


def poll_and_archive():
    latest_web3 = latest_web3_block()
    latest_db = latest_db_block()
    if latest_web3 > latest_db:
        for block in range(latest_db, latest_web3 + 1):
            print(f'Processing block {block}')

            contract_txes = get_block_contract_txes(block)
            for tx in contract_tx:
                write_contract_tx_bytecode(tx)
