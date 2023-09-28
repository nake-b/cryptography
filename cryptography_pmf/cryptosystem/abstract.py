from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional

from cryptography_pmf.coding import DefaultCharListEncoderDecoder, EncoderDecoder
from cryptography_pmf.commons import ALPHABET


class CryptoSystem(ABC):
    class Mode(Enum):
        ENCRYPT = "encrypt"
        DECRYPT = "decrypt"

    def __init__(
        self,
        default_key: Any,
        encoder_decoder: Optional[EncoderDecoder] = None,
    ):
        if encoder_decoder is None:
            encoder_decoder = DefaultCharListEncoderDecoder()
        self.default_key = default_key
        self._encoder_decoder = encoder_decoder

    def encrypt(self, open_text: str, key: Optional[Any] = None) -> str:
        return self.__perform_encryption_task(open_text, key, self.Mode.ENCRYPT)

    def decrypt(self, cypher: str, key: Optional[Any] = None) -> str:
        return self.__perform_encryption_task(cypher, key, self.Mode.DECRYPT)

    def __perform_encryption_task(
        self, text: str, key: Optional[Any], mode: Mode
    ) -> str:
        if key is None:
            key = self.default_key
        encoded_text = self._encoder_decoder.encode(text)
        encoded_transformed_text = (
            self._encrypt(encoded_text, key)
            if mode == self.Mode.ENCRYPT
            else self._decrypt(encoded_text, key)
        )
        transformed_text = self._encoder_decoder.decode(encoded_transformed_text)
        return transformed_text

    @abstractmethod
    def _encrypt(self, encoded_open_text: list, key) -> list:
        ...

    @abstractmethod
    def _decrypt(self, encoded_cypher: list[Any], key) -> list[Any]:
        ...

    def test(self, test_str: Optional[str] = None, key: Optional[Any] = None) -> bool:
        if test_str is None:
            test_str = "".join(ALPHABET)
        return self.decrypt(self.encrypt(test_str, key), key) == test_str.upper()
