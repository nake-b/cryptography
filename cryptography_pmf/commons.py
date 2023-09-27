from string import ascii_uppercase
from typing import Sequence

from mod import Mod

ALPHABET = list(ascii_uppercase)
MODULUS = len(ALPHABET)


def seq_to_mods(seq: Sequence) -> list[Mod]:
    return [Mod(s, MODULUS) for s in seq]
