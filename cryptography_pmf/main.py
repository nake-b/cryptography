from cryptography_pmf.cryptosystem.vigenere import AutoKeyVigenereCypher

if __name__ == "__main__":
    plain_text = "I love math"
    cs = AutoKeyVigenereCypher()
    cypher = cs.encrypt(plain_text)
    dec_plain_text = cs.decrypt(cypher)
    print(plain_text, cypher, dec_plain_text)


