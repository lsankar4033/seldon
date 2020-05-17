import logging
import sqlite3

from archivist.types import Transaction

# NOTE: change based on mount location of volume
DB_LOCATION = 'data.db'

logger = logging.getLogger('archivist.db')


class Database():
    def __init__(self, location=DB_LOCATION):
        self.location = location
        self._init_tables()

    def _init_tables(self):
        db = sqlite3.connect(self.location)
        c = db.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS contract_creations(
                block integer,
                tx_hash text,
                address text,
                bytecode blob)
                ''')
        c.execute('CREATE TABLE IF NOT EXISTS latest_block (block integer)')
        c.execute('CREATE TABLE IF NOT EXISTS manual_blocks (block integer)')

        db.commit()

    def manual_blocks(self):
        c = sqlite3.connect(self.location).cursor()
        records = list(c.execute('SELECT block FROM manual_blocks'))

        block_set = set()
        for record in records:
            block_set.add(record[0])

        return block_set

    def add_manual_block(self, block):
        db = sqlite3.connect(self.location)
        c = db.cursor()
        c.execute('INSERT INTO manual_blocks (block) VALUES (?)', (block,))
        db.commit()

        logger.info(f'updated latest block to {block}')

    def latest_block(self):
        c = sqlite3.connect(self.location).cursor()
        blocks = list(c.execute('SELECT block FROM latest_block ORDER BY block DESC LIMIT 1'))

        if len(blocks) == 0:
            return 0
        else:
            return blocks[0][0]

    def add_latest_block(self, block):
        db = sqlite3.connect(self.location)
        c = db.cursor()
        c.execute('INSERT INTO latest_block (block) VALUES (?)', (block,))
        db.commit()

        logger.info(f'updated latest block to {block}')

    def add_contract_creation(self, contract_creation_tx: Transaction):
        block = contract_creation_tx.block
        tx_hash = contract_creation_tx.hash
        address = contract_creation_tx.get_contract_address()
        bytecode = contract_creation_tx.data

        db = sqlite3.connect(self.location)
        c = db.cursor()
        c.execute('''INSERT INTO contract_creations
                (block, tx_hash, address, bytecode) VALUES
                (?, ?, ?, ?)''',
                  (block, tx_hash, address, bytecode))
        db.commit()

        logger.info(f'added contract creation for contract {address} with tx_hash {tx_hash}')
