from abc import ABC, abstractmethod
from typing import Any

from cryptography_pmf.commons import ALPHABET, reduce_str_to_alphabet


class EncoderDecoder(ABC):
    @abstractmethod
    def encode(self, x: str) -> list[Any]:
        ...

    @abstractmethod
    def decode(self, y: list[Any]) -> str:
        ...


class DefaultCharListEncoderDecoder(EncoderDecoder):
    def encode(self, x: str) -> list[str]:
        return list(x)

    def decode(self, y: list[str]) -> str:
        return "".join(y)


class Z26EncoderDecoder(EncoderDecoder):
    def __init__(self):
        assert len(ALPHABET) == 26
        self.__char_encode_map = {char: idx for idx, char in enumerate(ALPHABET)}
        self.__char_decode_map = {
            num: char for char, num in self.__char_encode_map.items()
        }

    def encode(self, x: str) -> list[int]:
        x = reduce_str_to_alphabet(x)
        return [self.__char_encode_map[char] for char in x]

    def decode(self, y: list[int]) -> str:
        chars = [self.__char_decode_map[n] for n in y]
        original = "".join(chars)
        return original
