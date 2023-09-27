from mod import Mod

from cryptography_pmf.coding import Z26EncoderDecoder
from cryptography_pmf.commons import MODULUS
from cryptography_pmf.cryptosystem.abstract import CryptoSystem


class AffineCypher(CryptoSystem):
    def __init__(self, default_key: tuple[int, int] = (17, 8)):
        encoder_decoder = Z26EncoderDecoder()
        super().__init__(default_key=default_key, encoder_decoder=encoder_decoder)

    def _encrypt(self, nums: list[int], key: tuple[int, int]) -> list[int]:
        self.__validate_key(key)
        a, b = key
        a = Mod(a, MODULUS)
        b = Mod(b, MODULUS)
        return [a * x + b for x in nums]

    def _decrypt(self, nums: list[int], key: tuple[int, int]) -> list[int]:
        self.__validate_key(key)
        a, b = key
        a = Mod(a, MODULUS)
        b = Mod(b, MODULUS)
        a_inv = 1 // a
        return [a_inv * (y - b) for y in nums]

    @staticmethod
    def __validate_key(key: tuple[int, int]):
        a, b = key
        try:
            _ = 1 // Mod(a, MODULUS)
        except ValueError as error:
            raise ValueError(
                f"Invalid key ({a}, {b}), {a} isn't invertible in Z26."
            ) from error
