import logging

from flask import Blueprint, Flask, jsonify

logger = logging.getLogger('archivist.manual_scrape_server')

scrape = Blueprint('scrape', __name__)

db = None
w3 = None


@scrape.route('/<int:block>', methods=['POST'])
def scrape_block(block):
    logger.info(f'manually scraping block {block}')

    txes = w3.block_to_txes(block)
    contract_creation_txes = [tx for tx in txes if tx.is_contract_creation()]

    logging.info(f'retrieved {len(contract_creation_txes)} contract creations for block {block}')
    for tx in contract_creation_txes:
        db.add_contract_creation(tx)

    db.add_manual_block(block)

    return jsonify({'contract_creation_count': len(contract_creation_txes)})


def create_server(injected_db, injected_w3):
    global db, w3
    db = injected_db
    w3 = injected_w3

    server = Flask(__name__)
    server.register_blueprint(scrape, url_prefix='/scrape')

    return server
