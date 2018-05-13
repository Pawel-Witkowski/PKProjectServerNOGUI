import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from math import gcd
import random
import Math_Modules


class AESCipher:

    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class RSA:
    def __init__(self):
        self.p = 33478071698956898786044169848212690817704794983713768568912431388982883793878002287614711652531743087737814467999489
        self.q = 36746043666799590428244633799627952632279158164343087642676032283815739666511279233373417143396810270092798736308917
        self.N = self.p * self.q
        self.e = self.generatePublic()
        self.d = self.generatePrivate()

    def generatePublic(self):
        return 913976530180265085042697477389115151869748071814837123379332008739392866713102250041200017676149556821235075470316986869464472195625810059634970920260874471356039519174314701524259881656553402746070368557994562881416288454072541823
        # fiValue = self.fiFunction()
        # checkedE = random.randrange(2, fiValue)
        # while gcd(checkedE, fiValue) != 1:
        #     checkedE = random.randrange(2, fiValue)
        # return checkedE

    def generatePrivate(self):
        return Math_Modules.modulo_multiplicative_inverse(self.e, self.fiFunction())

    def fiFunction(self):
        return (self.p - 1)*(self.q-1)

    def encryption(self, message):
        return Math_Modules.fast_power(message, self.e, self.N)

    def decryption(self, ciphertext):
        return Math_Modules.fast_power(ciphertext, self.d, self.N)


class DH:
    def __init__(self):
        self.p = 0xB10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371
        self.g = 0xA4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5
        self.privatePower = self.generatePrivatePower()
        self.publicKey = self.generatePublicKey()

    def generatePrivatePower(self):
        return random.randrange(2, self.p - 1)

    def generatePublicKey(self):
        return Math_Modules.fast_power(self.g, self.privatePower, self.p)

    def generatePrivateKey(self, value):
        self.privateKey = Math_Modules.fast_power(value, self.privatePower, self.p)


def powerModulo(message, power, modulo):
    return Math_Modules.fast_power(message, power, modulo)

def hashMessageToInt(message):
    m = hashlib.sha256()
    m.update(message.encode())
    h = m.hexdigest()
    return int(h, 16)

def hashBytesToInt(bytes):
    m = hashlib.sha256()
    m.update(bytes)
    h = m.hexdigest()
    return int(h, 16)

def packMessage(bytes, signKey, modulo):
    from json import dumps
    hashedMessage = hashBytesToInt(bytes)
    signature = powerModulo(hashedMessage, signKey, modulo)
    packed = {
            'message': bytes.decode(),
            'signature': signature
           }
    # print(hashedMessage)
    return dumps(packed)

def verifySignature(signature, message, key, modulo):
    hashedMessage = hashMessageToInt(message)
    decryptedSignature = powerModulo(signature, key, modulo)
    return hashedMessage == decryptedSignature