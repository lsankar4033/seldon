import sqlite3

from archivist.types import Transaction

# NOTE: change based on mount location of volume
DB_LOCATION = 'data.db'


class Database():
    def __init__(self, location=DB_LOCATION):
        self.db = sqlite3.connect(location)
        self._init_tables()

    def _init_tables(self):
        c = self.db.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS contract_creations(
                block integer,
                tx_hash text,
                address text,
                bytecode blob)
                ''')
        c.execute('CREATE TABLE IF NOT EXISTS latest_block (block integer)')

        self.db.commit()

    def latest_block(self):
        c = db.cursor()
        blocks = list(c.execute('SELECT block FROM latest_block ORDER BY block DESC LIMIT 1'))

        if len(blocks) == 0:
            return 0
        else:
            return blocks[0][0]

    def add_latest_block(self, b):
        c = self.db.cursor()
        c.execute('INSERT INTO latest_block (block) VALUES (?)', (b,))
        self.db.commit()
        return b

    def add_contract_creation(self, contract_creation_tx: Transaction):
        block = contract_creation_tx.block
        tx_hash = contract_creation_tx.hash
        address = contract_creation_tx.get_contract_address()
        bytecode = contract_creation_tx.data

        c = self.db.cursor()
        c.execute('''INSERT INTO contract_creations
                (block, tx_hash, address, bytecode) VALUES
                (?, ?, ?, ?)''',
                  (block, tx_hash, address, bytecode))
        self.db.commit()

    def contract_by_address(self, address: str):
        # NOTE: for testing the db, perhaps just a temp method
        c = self.db.cursor()
        c.execute('SELECT * from contract_bytecode WHERE address=?', (address,))

        return c.fetchone()
