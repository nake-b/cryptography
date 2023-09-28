# cryptography
Python package that follows the "Cryptography" course held at the Mathematics and Computer Science study programme, Prirodno-matematički fakultet, Univerzitet u Tuzli.

## How to install
1. Create and activate conda environment.
```shell
conda create -n cryptography_pmf python=3.10
conda activate cryptography_pmf
```
2. Install the package.
```shell
pip install -e .
```

## Example usage

```python
from cryptography_pmf.cryptosystem.playfair import PlayfairCypher

plain_text = "I love math"
playfair = PlayfairCypher(default_key="PMFUNTZ")
cypher = playfair.encrypt(plain_text)  # = GQLXKZBZOU
dec_plain_text = playfair.decrypt(cypher)  # = ILOVEMATHX

```
