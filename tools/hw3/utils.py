from SPN_copy import pi_s,pi_p,l,m

pi_s_reverse = {v: k for k, v in pi_s.items()}  # 输入是int，输出也是，
pi_p_reverse = {value:key for key,value in pi_p.items()}

# 小函数们


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
    对两个长度为相同的01字符串进行异或, 以字符串返回异或结果

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
    for i, key in enumerate(key_bin):
        if not check_one_dif(key, y_block[i], y_star_block[i], diffs[i]):
            return False
    return True




def reverse_permutation(v:str):
    """
    逆置换，输入输出都为str，长度16
    """
    res = [None] * l * m
    tmp_v = list(map(int, v))
    for i in range(l * m):
        res[pi_p_reverse[i+1]] = tmp_v[i] #键是 1-16 故+1
    return res

def reverse_substitution(u:str):
    """
    逆代换，输入输出为str，长度16
    """
    tmp_u = list(map(int,u))
    v = []
    for i in range(m):
        tmp = tmp_u[4 * i : 4 * i + l]
        before_pi_s = int("".join(str(tmp[i]) for i in range(4)), base=2)
        after_pi_s = pi_s_reverse[before_pi_s]  # 应该不会出事的...
        v.extend(list(f"{after_pi_s:04b}"))
    return "".join(v) # v里面是字符串，把它们合起来。
    # return [int(item) for item in v]

def get_reverse_func(cur_K, n):
    def reverse(y):
        v4 = xor(y,''.join(cur_K[4:8]))
        u4 = reverse_substitution(v4)
        if n == 1:
            return u4
        w3 = xor(u4, ''.join(cur_K[3:7]))
        v3 = reverse_permutation(w3)
        u3 = reverse_substitution(v3)
        if n == 2:
            return u3
        w2 = xor(u2, ''.join(cur_K[2:6]))
        v2 = reverse_permutation(w2)
        u2 = reverse_substitution(v2)
        if n == 3:
            return u2
        w1 = xor(u1, ''.join(cur_K[1:5]))
        v1 = reverse_permutation(w1)
        u1 = reverse_substitution(v1)
        if n == 4:
            return u1
    return reverse
