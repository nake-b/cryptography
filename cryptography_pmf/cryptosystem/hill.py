import numpy as np
from mod import Mod
from sympy import Matrix

from cryptography_pmf.coding import Z26EncoderDecoder
from cryptography_pmf.commons import seq_to_mods
from cryptography_pmf.cryptosystem.abstract import CryptoSystem


class HillCypher(CryptoSystem):
    def __init__(
        self, default_key: np.ndarray = np.array([[2, 17, 9], [23, 1, 15], [14, 6, 11]])
    ):
        encoder_decoder = Z26EncoderDecoder()
        super().__init__(default_key=default_key, encoder_decoder=encoder_decoder)

    def _encrypt(self, x: list[int], key: np.ndarray) -> list[int]:
        return self.__transform(x, key)

    def _decrypt(self, y: list[int], key: np.ndarray) -> list[int]:
        inv_key = self.__invert_matrix_modular(key)
        return self.__transform(y, inv_key)

    def __transform(self, x: list[int], key: np.ndarray) -> list[int]:
        mods = seq_to_mods(x)
        m = key.shape[0]
        X = self.__mods_to_matrix(mods, m)
        Y = X @ key
        y = Y.reshape(-1)
        y = [yi % 26 for yi in y]
        return y

    def __mods_to_matrix(self, mods: list[Mod], m: int) -> np.array:
        num_chars_to_add = len(mods) % m
        if num_chars_to_add > 0:
            chars_to_add = num_chars_to_add * "Z"
            mods_to_add = self._encoder_decoder.encode(chars_to_add)
            mods += mods_to_add
        x = np.array([int(mod) for mod in mods])
        X = x.reshape((len(x) // m, m))
        return X

    def __invert_matrix_modular(self, mat: np.ndarray, mod: int = 26) -> np.ndarray:
        sympy_mat = Matrix(mat)
        sympy_inv_mat = sympy_mat.inv_mod(mod)
        np_inv_mat = np.array(sympy_inv_mat)
        return np_inv_mat
