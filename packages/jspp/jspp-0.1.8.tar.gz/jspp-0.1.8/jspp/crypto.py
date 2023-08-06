"""Crypto"""

def caesar_decrypt(string_encrypted, rot):
    space = []
    caesartxt = string_encrypted.split()
    result = []
    for joinedchars in caesartxt:
        caesarord = [ord(x) for x in joinedchars]
        txtplainord = [o - rot for o in caesarord]
        txtplainchars = [chr(i) for i in txtplainord]
        result.append("".join(txtplainchars))
    result = "".join(result)
    return result

def caesar_encrypt(string, rot):
    result = []
    for x in range(len(string)):
        current_character = string[x]
        if(current_character.isupper()):
            result.append("".join(chr((ord(current_character)+rot-65)%26+65)))
        else:
            result.append("".join(chr((ord(current_character)+rot-97)%26+97)))
    result = "".join(result)
    return result

def bin2text(text):
    def chkstr(string, length):
        return (string[0+i:length+i] for i in range(0, len(string), length))
    final_text = str(text).replace(" ","")
    result = ""
    for txw in chkstr(final_text, 8):
        txw = int(txw, 2)
        char = chr(txw)
        result += char
    return result

def text2bin(text):
    return " ".join(format(ord(x), "b") for x in text)

def hex2text(text):
    return "".join([chr(int("".join(c), 16)) for c in zip(text[0::2],text[1::2])])

def text2hex(text):
    return "".join([hex(ord(i)) for i in text]).replace("0x", "")

def clean_text2hex(text):
    return "".join([str(hex(ord(i)))[2:4] for i in text])