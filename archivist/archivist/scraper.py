import logging
import time

LOOP_WAIT_SECS = 60

logger = logging.getLogger('archivist.scraper')


def scraper_loop(db, w3):
    while True:
        latest_db_block = db.latest_block()
        latest_web3_block = w3.latest_block()
        logging.info(f'found latest db block: {latest_db_block} and latest w3 block: {latest_web3_block}')
        if latest_web3_block > latest_db_block:
            for block in range(latest_db_block + 1, latest_web3_block + 1):
                logging.info(f'retrieving txes for block {block}')
                txes = w3.block_to_txes(block)
                contract_creation_txes = [tx for tx in txes if tx.is_contract_creation()]

                logging.info(f'retrieved {len(contract_creation_txes)} contract creations for block {block}')
                for tx in contract_creation_txes:
                    db.add_contract_creation(tx)

            db.add_latest_block(latest_web3_block)

        logging.info(f'sleeping for {LOOP_WAIT_SECS}')
        time.sleep(LOOP_WAIT_SECS)
