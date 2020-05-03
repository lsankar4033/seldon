
from pyevmasm import Instruction, disassemble_all

from typing import List


def parse_instructions(bytecode) -> List[Instruction]:
    return [i for i in disassemble_all(bytecode)]

# TODO: use rattle
