def vigenere_decrypt(ciphertext, key):
    decrypted_text = []
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():  # 只处理字母
            shift = key[i % key_length]  # 获取当前密钥字母的偏移
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))  # 进行解密
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)  # 非字母字符直接添加
    return ''.join(decrypted_text)

# 密钥
# key = [7, 19, 22, 12, 9, 2]
key = [19, 7, 4, 14, 17, 24 ]
# 密文
ciphertext = """
BNVSNSIHQCEELSSKKYERIFJKXUMBGYKAMQLJTYAVFBKVT 
DVBPVVRJYYLAOKYMPQSCGDLFSRLLPROYGESEBUUALRWXM 
MASAZLGLEDFJBZAVVPXWICGJXASCBYEHOSNMULKCEAHTQ 
OKMFLEBKFXLRRFDTZXCIWBJSICBGAWDVYDHAVFJXZIBKC 
GJIWEAHTTOEWTUHKRQVVRGZBXYIREMMASCSPBNLHJMBLR 
FFJELHWEYLWISTFVVYFJCMHYUYRUFSFMGESIGRLWALSWM 
NUHSIMYYITCCQPZSICEHBCCMZFEGVJYOCDEMMPGHVAAUM 
ELCMOEHVLTIPSUYILVGFLMVWDVYDBTHFRAYISYSGKVSUU 
HYHGGCKTMBLRX 
"""

# 移除非字母字符（仅解密字母部分）
ciphertext = ''.join([char for char in ciphertext if char.isalpha()])

# 解密
decrypted_text = vigenere_decrypt(ciphertext, key)
print(decrypted_text)
