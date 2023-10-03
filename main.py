from Crypto.Cipher import AES
from tqdm.contrib.concurrent import process_map
from itertools import repeat
from time import monotonic

import base64
import sys
import datetime


def zeropadding(data, block_size):
    add = len(data) % block_size
    # BEHOLD! An if-statement that is so important that overlooking it led to me wasting TENS OF HOURS!
    if add == 0:
        return data
    padding = b"\x00" * (block_size - add)
    return data + padding


def aes_encrypt_ecb(key, plaintext):
    padded_key = zeropadding(key.encode('utf-8'), AES.block_size)
    cipher = AES.new(padded_key, AES.MODE_ECB)
    padded_data = zeropadding(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(ciphertext).decode('utf-8')


def aes_decrypt_ecb(key, ciphertext):
    padded_key = zeropadding(key.encode('utf-8'), AES.block_size)
    cipher = AES.new(padded_key, AES.MODE_ECB)
    ciphertext = base64.b64decode(ciphertext)
    padded_data = cipher.decrypt(ciphertext)
    return padded_data.rstrip(b"\x00").decode("utf-8")


def worker(i, main_key):
    for j in range(0x20, 0x7F):
        for k in range(0x20, 0x7F):
            for l in range(0x20, 0x7F):
                try:
                    key = main_key.replace('▆', chr(i), 1).replace('▆', chr(j), 1).replace('▆', chr(k), 1).replace('▆', chr(l), 1)
                    plaintext = aes_decrypt_ecb(key, ciphertext)
                    print("一可能合理金鑰為:", key)
                    print("一可能合理明文為:", plaintext)
                    # Since there could be many possible result that is valid, the loop doesn't end here.
                except UnicodeDecodeError:
                    pass


if __name__ == '__main__':
    # Check If the setting is good. 
    # Test pre-setting
    key = '123456789'
    plaintext = "security"

    ciphertext = aes_encrypt_ecb(key, plaintext)
    print("測試密文結果為:", ciphertext) # It should be "pKjVPv28yVMn5cRXeUNYpg==".
    if ciphertext != "pKjVPv28yVMn5cRXeUNYpg==":
        sys.exit("wrong ciphertext.")
    else:
        print("加密功能 OK!")

    plaintext = aes_decrypt_ecb(key, ciphertext)
    print("測試明文結果為:", plaintext) # It should be "security".
    if plaintext != "security":
        sys.exit("wrong plaintext.")
    else:
        print("解密功能 OK!")

    # The question set
    ciphertext_set = {
        0: "2NHkjlDyk82JBke5q8CnMQZ1iiHID8QEst+/Ld6lWFMP5omXXh/1LnmrYKOD04idKfzfL+6C96391/iN7+X0eg==",
        1: "INNkAZHIpe5u9LvzhH24VyORcZQVDCFXzV6V/l9M7rpgqskMxvaRbGwR2dZaxMDZ",
        2: "NnJyrVT80DxOU5jOxHdZ9NRlaLPRhaAUYANfaVACUeqcrPoXz5eeTs9m6X2fVJC9SJ+X03mu3zD/WTiUjwzIyg==",
        3: "89NEvN56VtNjo1w5x3whmFUOZOqTaRyoMnIrPjCGKUv5n7kgGFHDmStzEgDFAU7QnZOK9MLeO/FW4etzIOhpKfOsw5xSD4Em72X1O2FRfaM=",
        4: "FZp57a6p84EUNC7I/ENj4RhPZtryOJr4che9JbA8ng1eI8ZMTlsl8kzicBDqkOqkFj3lwC69KR2MeA8lscVlig=="
    }

    while True:
        student_id = input("------------------------\n請輸入您的成大學號: ") # my id
        try:
            if len(student_id) == 9:
                ciphertext = ciphertext_set[int(student_id[-1]) % 5]
                break
            else:
                print("學號格式並不正確，請您再試一次。")
        except ValueError:
            print("學號格式並不正確，請您再試一次。")
        except IndexError:
            print("學號格式並不正確，請您再試一次。")

    print("所屬密文為:", ciphertext)

    key_set = {
        0: "$\"▆vXl▆K▆\/ {9Fp▆",
        1: "0lOS▆b] ▆&N) ▆w▆@+",
        2: "Bk▆fom] ▆H▆ (J▆'|,",
        3: "2▆? ▆mYD;@▆;x▆v\"i",
        4: "|q▆~k=▆&?I$Fx▆N▆"
    }
    main_key = key_set[int(student_id[8]) % 5]
    print("所屬金鑰為:", main_key)

    # Start solving
    print("破解開始！")
    start = monotonic()
    process_map(worker, range(0x20, 0x7F), repeat(main_key), max_workers=4)
    end = monotonic()
    SecToConvert = end - start
    ConvertedSec = str(datetime.timedelta(seconds = SecToConvert))
    print("所耗費總時長為:", ConvertedSec)
