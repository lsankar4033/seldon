from archivist.db import Database
from archivist.w3 import W3


def archive_loop(db, w3):
    latest_db_block = db.latest_block()
    latest_web3_block = w3.latest_block()
    # TODO: log latest blocks
    if latest_web3_block > latest_db_block:
        # TODO: log how many blocks we're about to scrape
        for block in range(latest_db, latest_web3 + 1):
            # TODO: log which block we're about to process

            txes = w3.block_to_txes()
            contract_creation_txes = [tx for tx in txes if tx.is_contract_creation()]
            # TODO: log how many txes we found and how many contract creation txes
            for tx in contract_creation_txes:
                # TODO: log adding this thing to db
                db.add_contract_creation(tx)


if __name__ == '__main__':
    db = Database()
    w3 = W3()
    archive_loop(db, w3)
