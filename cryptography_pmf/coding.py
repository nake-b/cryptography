from abc import ABC, abstractmethod
from typing import Any

from cryptography_pmf.commons import ALPHABET


class EncoderDecoder(ABC):
    def encode(self, x: str) -> list[Any]:
        x = self._clean_input(x)
        return self._encode(x)

    @abstractmethod
    def _encode(self, x: str) -> list[Any]:
        ...

    def decode(self, y: list[Any]) -> str:
        return self._decode(y)

    @abstractmethod
    def _decode(self, y: list[Any]) -> str:
        ...

    @staticmethod
    def _clean_input(x: str) -> str:
        alpha_str = "".join(filter(str.isalpha, x))
        upper_alpha_str = alpha_str.upper()
        return upper_alpha_str


class Z26EncoderDecoder(EncoderDecoder):
    def __init__(self):
        assert len(ALPHABET) == 26
        self.__char_encode_map = {char: idx for idx, char in enumerate(ALPHABET)}
        self.__char_decode_map = {
            num: char for char, num in self.__char_encode_map.items()
        }

    def _encode(self, x: str) -> list[int]:
        return [self.__char_encode_map[char] for char in x]

    def _decode(self, y: list[int]) -> str:
        chars = [self.__char_decode_map[n] for n in y]
        original = "".join(chars)
        return original
