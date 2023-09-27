from typing import Optional

from mod import Mod

from cryptography_pmf.coding import Z26EncoderDecoder
from cryptography_pmf.commons import MODULUS
from cryptography_pmf.cryptosystem.abstract import CryptoSystem


class CaesarCypher(CryptoSystem):
    def __init__(self, default_key: int = 3):
        encoder_decoder = Z26EncoderDecoder()
        super().__init__(default_key=default_key, encoder_decoder=encoder_decoder)

    def _encrypt(self, nums: list[int], key: int) -> list[int]:
        key = Mod(key, MODULUS)
        return [int(num + key) for num in nums]

    def _decrypt(self, nums: list[int], key: int) -> list[int]:
        key = Mod(key, MODULUS)
        return [int(num - key) for num in nums]
