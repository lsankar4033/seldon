
from pyevmasm import Instruction, disassemble_all

from typing import List


def parse_instructions(bytecode) -> List[Instruction]:
    # NOTE: I may choose to use rattle under the hood in the future
    return [i for i in disassemble_all(bytecode)]
