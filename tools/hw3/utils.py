from SPN_copy import pi_s

pi_s_reverse = {v: k for k, v in pi_s.items()}  # 输入是数字，输出也是，


def get_differential(delta_x):
    """
    返回一个生成器以获取(x, x*)的元组, 其异或等于delta_x

    Args:
        delta_x (str) : 输入异或, 长度为16

    Returns:
        xor_pair (tuple(x,x*)) : 异或为 delta_x 的两个字符串
    """
    # cur_time = 0
    for i in range(2**16):
        x = f"{i:016b}"
        # cur_time +=1
        # print(cur_time)
        yield (x, xor(x, delta_x))


def xor(a: str, b: str):
    """
    对两个长度为4的01字符串进行异或, 以字符串返回异或结果

    Args
        a(str)
        b(str)

    Returns
        str

    """
    a_int = int(a, base=2)
    b_int = int(b, base=2)
    result = a_int ^ b_int
    return format(result, f"0{len(a)}b")

def check_one_dif(L, y_block, y_star_block, dif):
    v = xor(L, y_block)
    u = f"{pi_s_reverse[int(v,base = 2)]:04b}"
    v_star = xor(L, y_star_block)
    u_star = f"{pi_s_reverse[int(v_star,base = 2)]:04b}"
    u_dif = xor(u, u_star)
    return u_dif == dif


def is_dif_satisfy(key_bin, y_block, y_star_block, diffs):
    for i,key in enumerate(key_bin):
        if not check_one_dif(key, y_block[i], y_star_block[i] ,diffs[i]):
            return False
    return True



