
from pyevmasm import Instruction, disassemble_all

from typing import List


def parse_instructions(bytecode, reduce=False) -> List[Instruction]:
    # NOTE: I may choose to use rattle under the hood in the future
    # TODO: use rattle to get reduced rep. I can test reduced reps against the full rep manually
    return [i for i in disassemble_all(bytecode)]
