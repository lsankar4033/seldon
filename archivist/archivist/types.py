import rlp
from eth_hash.auto import keccak
from eth_utils.conversions import to_hex
from eth_utils.hexadecimal import decode_hex

from typing import NamedTuple


def _force_bytes_to_address(value: bytes):
    trimmed_value = value[-20:]
    padded_value = trimmed_value.rjust(20, b'\x00')

    return to_hex(padded_value)


class Transaction(NamedTuple):
    block: int
    hash: str
    from_address: str
    to_address: str
    nonce: int
    data: bytes

    def is_contract_creation(self):
        return self.to_address is None

    def get_contract_address(self) -> str:
        if not self.is_contract_creation():
            return '0x0'

        rlp_encoded = rlp.encode([decode_hex(self.from_address), self.nonce])
        hashed = keccak(rlp_encoded)

        return _force_bytes_to_address(hashed)
