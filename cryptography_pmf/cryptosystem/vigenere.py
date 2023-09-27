from abc import ABC

from mod import Mod

from cryptography_pmf.coding import Z26EncoderDecoder
from cryptography_pmf.commons import seq_to_mods
from cryptography_pmf.cryptosystem.abstract import CryptoSystem


class VigenereCypher(CryptoSystem, ABC):
    def __init__(self, default_key: str = "PMFTZ"):
        encoder_decoder = Z26EncoderDecoder()
        super().__init__(default_key=default_key, encoder_decoder=encoder_decoder)

    def _key_to_mods(self, key: str) -> list[Mod]:
        key_nums = self._encoder_decoder.encode(key)
        key_mods = seq_to_mods(key_nums)
        return key_mods


class RepeatingKeyVigenereCypher(VigenereCypher):
    def _encrypt(self, nums: list[int], key: str) -> list[int]:
        key_mods = self._key_to_mods(key)
        return [num + key_mods[idx % len(key_mods)] for idx, num in enumerate(nums)]

    def _decrypt(self, nums: list[int], key: str) -> list[int]:
        key_mods = self._key_to_mods(key)
        return [num - key_mods[idx % len(key_mods)] for idx, num in enumerate(nums)]


class AutoKeyVigenereCypher(VigenereCypher):
    def _encrypt(self, nums: list[int], key: str) -> list[int]:
        key_mods = self._key_to_mods(key)
        nums = seq_to_mods(nums)
        result_key_part = [num + key_num for num, key_num in zip(nums, key_mods)]
        result_auto_part = [
            nums[i] + nums[i - len(key)] for i in range(len(key), len(nums))
        ]
        result = result_key_part + result_auto_part
        return result

    def _decrypt(self, nums: list[int], key: str) -> list[int]:
        key_mods = self._key_to_mods(key)
        result = [num - key_num for num, key_num in zip(nums, key_mods)]
        for idx in range(len(key), len(nums)):
            char = nums[idx] - result[idx - len(key)]
            result.append(char)
        return result
