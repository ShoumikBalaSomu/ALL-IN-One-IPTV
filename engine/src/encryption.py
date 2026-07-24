import base64

class EncryptionVault:
    @staticmethod
    def xor_crypt(data: str, key: str = "secret") -> str:
        res = []
        for i, c in enumerate(data):
            res.append(chr(ord(c) ^ ord(key[i % len(key)])))
        return base64.b64encode("".join(res).encode()).decode()

    @staticmethod
    def xor_decrypt(data: str, key: str = "secret") -> str:
        raw = base64.b64decode(data.encode()).decode()
        res = []
        for i, c in enumerate(raw):
            res.append(chr(ord(c) ^ ord(key[i % len(key)])))
        return "".join(res)
