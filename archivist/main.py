import sqlite3

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


# NOTE: just for testing
def reset_latest_block():
    c = db.cursor()
    c.execute('DELETE FROM latest_block')
    db.commit()


def latest_web3_block():
    # NOTE: take actual latest - N, to provide re-org protection
    web3_response = w3.eth.getBlock('latest')
    return web3_response.number


def poll_and_archive():
    latest_web3 = latest_web3_block()
    latest_db = latest_db_block()
    if latest_web3 > latest_db:
        # for latest_db -> latest_web3, attempt to get contract data and store in db
        # log each block processed where a contract lives
        ...
