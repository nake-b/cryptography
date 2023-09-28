from string import ascii_uppercase
from typing import Sequence

from mod import Mod

ALPHABET = list(ascii_uppercase)
MODULUS = len(ALPHABET)


def reduce_str_to_alphabet(s: str | list[str]) -> str:
    valid_chars = [c for c in s.upper() if c in ALPHABET]
    reduced = "".join(valid_chars)
    return reduced


def seq_to_mods(seq: Sequence) -> list[Mod]:
    return [Mod(s, MODULUS) for s in seq]
