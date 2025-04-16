from utils import sbox, rcon

Nr = 10


def AES128_Encrypt(x:str, K:str): # 16进制的字符串
    expanded_key = KeyExpansion(K)
    RoundKeys = ["".join(expanded_key[4*i:4*i+4]) for i in range(11)]
    State = x
    State = AddRoundKey(State, RoundKeys[0])
    for i in range(Nr-1):
        State = SubBytes(State)
        State = ShiftRows(State)
        State = MixColumns(State)
        State = AddRoundKey(State, RoundKeys[i+1])
    State = SubBytes(State)
    State = ShiftRows(State)
    State = AddRoundKey(State, RoundKeys[10]) 
    y = State
    return y


def AddRoundKey(State:str, RoundKey:str):
    return xor(State, RoundKey)



def SubBytes(State:str):
    output = []
    for i in range(16):
        byte =  State[2*i:2*i+2]
        output.append(format(sbox[int(byte, base= 16)], "02X") )
        f""
        
        
    return "".join(output)
        


def ShiftRows(State:str):
    Slices = [[ State[2*i+8*j:2*i+8*j + 2] for j in range(4)] for i in range(4)]
    Slices[1] = Slices[1][1:] + Slices[1][:1]
    Slices[2] = Slices[2][2:] + Slices[2][:2]
    Slices[3] = Slices[3][3:] + Slices[3][:3]
    output = []
    for i in range(4):
        for j in range(4):
            output.append(Slices[j][i])
    return "".join(output)



def MixColumns(State:str):
    State_cols = [[State[8*i+2*j:8*i+2*j+2] for j in range(4) ] for i in range(4)]
    output = []
    u = 4*[None]
    t = 4*[None]
    a = 2
    b = 3
    for k in range(4):
        for i in range(4):
            t[i] = State_cols[k][i]
        
        for i in range(4):
            u[i] = xor(gf_mul(a,t[i%4]), gf_mul(b,t[(1+i)%4]))
            u[i] = xor(u[i], t[(2+i)%4])
            u[i] = xor(u[i], t[(3+i)%4])
        output.extend(u)
    return "".join(output)
    
def gf_mul(a: str, b: str) -> str:
    if type(a) == str:
        a = int(a, base = 16)
    if type(b) == str:
        b = int(b, base= 16)
    p = 0
    for _ in range(8):
        if b & 1:  # 如果 b 的最低位是 1
            p ^= a  # p 与 a 异或
        hi_bit_set = a & 0x80  # 检查 a 的最高位
        a = (a << 1) & 0xFF  # 左移 1 位并保持 8 位
        if hi_bit_set:  # 如果最高位是 1
            a ^= 0x1b  # 模多项式约减
        b >>= 1  # b 右移 1 位
    return format(p, '02x')



def KeyExpansion(Orig_Key:str):
    key = [Orig_Key[2*i:2*i+2] for i in range(16)]
    w = [None]*44
    for i in range(4):
        w[i] = "".join(key[4*i:4*i+4])
    for i in range(4,44):
        temp = w[i-1]
        if  i%4 == 0:
            temp = xor(SubWord(RotWord(temp)),f"{rcon[i//4]:08X}")
        w[i] = xor(w[i-4], temp)
    return w

def RotWord(part_of_key:str): # 4字节
    parts = [part_of_key[2*i:2*i+2] for i in range(4)]
    temp = parts[0]
    parts[0] = parts[1]
    parts[1] = parts[2]
    parts[2] = parts[3]
    parts[3] = temp
    return "".join(parts)
    

def SubWord(part_of_key:str): # 4 字节
    output = []
    for i in range(4):
        output.append(format(sbox[int(part_of_key[2*i:2*i+2], base= 16)], "02X"))
    return "".join(output)

def xor(a:str,b:str): # 16进制的

    a_int = int(a, base=16)
    b_int = int(b, base=16)
    result = a_int ^ b_int
    return format(result, f"0{len(a)}X")


AES128_Encrypt("00112233445566778899aabbccddeeff", "000102030405060708090a0b0c0d0e0f")