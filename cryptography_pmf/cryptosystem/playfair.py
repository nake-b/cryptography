from enum import Enum

import numpy as np
from cryptography_pmf.coding import DefaultCharListEncoderDecoder
from cryptography_pmf.commons import ALPHABET, reduce_str_to_alphabet
from cryptography_pmf.cryptosystem.abstract import CryptoSystem
from mod import Mod


class PlayfairEncryptor(CryptoSystem):
    class InvalidInputError(Exception):
        ...

    class TransformMode(Enum):
        ENCRYPT = "encrypt"
        DECRYPT = "decrypt"

    def __init__(self, default_key: str = "MATHEMATICS"):
        default_key = reduce_str_to_alphabet(default_key)
        encoder_decoder = (
            DefaultCharListEncoderDecoder()
        )  # Playfair works with strings/characters
        super().__init__(default_key=default_key, encoder_decoder=encoder_decoder)

    def __construct_key_matrix(self, key) -> np.ndarray[str]:
        unique_key_chars = []
        for char in key:
            if char not in unique_key_chars:
                unique_key_chars.append(char)
        char_left = set(ALPHABET).difference(set(unique_key_chars))
        char_left = sorted(char_left)
        char_left.remove("W")
        key_vector = unique_key_chars + list(char_left)
        assert len(key_vector) == 25
        key_matrix = np.reshape(key_vector, (5, 5))
        return key_matrix

    def _encrypt(self, x: list[str], key: str) -> str:
        return self.__transform_str(x, key, self.TransformMode.ENCRYPT)

    def _decrypt(self, y: list[str], key: str) -> str:
        return self.__transform_str(y, key, self.TransformMode.DECRYPT)

    def __preprocess_plain_text(self, plain_text_chars: list[str]) -> str:
        plain_text = "".join(plain_text_chars)
        plain_text = reduce_str_to_alphabet(plain_text)
        # Remove pairwise duplicates
        i = 0
        while i + 1 < len(plain_text):
            char, next_char = plain_text[i], plain_text[i + 1]
            if char == next_char:
                plain_text = plain_text[: i + 1] + "X" + plain_text[i + 1 :]
            i += 2
        # Ensure parity of length
        if len(plain_text) % 2 == 1:
            plain_text += "X"
        return plain_text

    def __char_to_matrix_coords(
        self, c: str, key_matrix: np.ndarray
    ) -> tuple[Mod, Mod]:
        item_index: np.ndarray[list[int], list[int]] = np.where(
            key_matrix == c
        )  # item_index = ([i], [j])
        i = item_index[0][0]
        j = item_index[1][0]
        return Mod(i, 5), Mod(j, 5)

    def __transform_str(self, x: list[str], key: str, mode: TransformMode) -> str:
        key = reduce_str_to_alphabet(key)
        cypher = ""
        m = self.__construct_key_matrix(key)
        if mode == self.TransformMode.ENCRYPT:
            x = self.__preprocess_plain_text(x)
        for c1, c2 in zip(x[::2], x[1::2]):
            try:
                y1, y2 = self.__transform_char_pair(c1, c2, m, mode)
            except self.InvalidInputError as e:
                raise ValueError(f"Invalid input: {x}") from e
            cypher = cypher + y1 + y2
        return cypher

    def __transform_char_pair(
        self, c1: str, c2: str, key_matrix: np.ndarray, mode: TransformMode
    ):
        if c1 == c2:
            raise self.InvalidInputError(
                f"Adjacent characters that are being transformed must not be identical."
            )
        i1, j1 = self.__char_to_matrix_coords(c1, key_matrix)
        i2, j2 = self.__char_to_matrix_coords(c2, key_matrix)
        shift = 1 if mode == self.TransformMode.ENCRYPT else -1
        if i1 == i2:
            j1 += shift
            j2 += shift
        elif j1 == j2:
            i1 += shift
            i2 += shift
        else:
            j1, j2 = j2, j1
        return key_matrix[int(i1), int(j1)], key_matrix[int(i2), int(j2)]
