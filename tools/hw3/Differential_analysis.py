from SPN_copy import spn, pi_s, pi_p
from itertools import product


# 解包顺序要看看啊，这一回好歹是claude救了我，

pi_s_reverse = {v: k for k, v in pi_s.items()}  # 输入是数字，输出也是，

# 这里，我们的 x 和 x* 的长度 是16， 2


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


def get_T_set(xor_gen, K):
    # cur_time = 0
    for x, x_star in xor_gen:
        x_intlist = [int(num) for num in x]
        x_star_intlist = [int(num) for num in x_star]
        y_intlist = spn(x_intlist, K)
        y_star_intlist = spn(x_star_intlist, K)
        y = "".join(map(str, y_intlist))
        y_star = "".join(map(str, y_star_intlist))
        # cur_time += 1
        # print("H",cur_time)
        yield (x, x_star, y, y_star)


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

def differential_attack(T_set, times, dif1=None, dif2=None, dif3=None, dif4=None):
    key_candidate = {}
    # for i in range(16):
    #     for j in range(16):
    #         key_candidate[(f"{i:04b}", f"{j:04b}")] = 0
    
    active_indices = [i for i, d in enumerate(diffs) if d is not None]
    diffs = [dif1, dif2, dif3, dif4]
    cur_time = 0  # 有效次数....
    for _, _, y, y_star in T_set:  # Fixed: corrected unpacking order to match get_T_set
        # 过滤，提高效率，但不是必须的
        is_effective = True
        for i, dif in enumerate(diffs):
            if dif == None and y[4*i:4*i+4] != y_star[4*i:4*i+4]:
                is_effective = False
                break
        
        # 正式比对,检查差分是否满足要求。
        if is_effective:
            # 选取需要比对的
            y_block = [y[4*i:4*i+4] for i in range(4) if diffs[i] != None ]
            y_star_block = [y_star[4*i:4*i+4] for i in range(4) if diffs[i] != None]
            
            for key_bin in key_candidate:
                if is_dif_satisfy(key_bin, y_block, y_star_block ,diffs):
                    key_candidate[key_bin] +=1
                
                # 计数，T到一定大小就比较准确了，可以控制不要用那么多。
                cur_time +=1
                if cur_time >= times:
                    break

    max = -1
    maxkey = None
    for L1, L2 in key_candidate:
        if key_candidate[(L1, L2)] > max:
            max = key_candidate[(L1, L2)]
            maxkey = (L1, L2)
    return maxkey


def differential_attack2(T_set, times):
    key_candidate = {}
    for i in range(16):
        for j in range(16):
            key_candidate[(f"{i:04b}", f"{j:04b}")] = 0

    cur_time = 0  # 有效次数....
    for (
        x,
        x_star,
        y,
        y_star,
    ) in T_set:  # Fixed: corrected unpacking order to match get_T_set
        if y[4:8] == y_star[4:8]:
            for L1, L2 in key_candidate:
                if is_:
                    key_candidate[(L1, L2)] += 1
                v2 = xor(L1, y[4:8])
                v4 = xor(L2, y[12:16])
                u2 = f"{pi_s_reverse[int(v2,base = 2)]:04b}"
                u4 = f"{pi_s_reverse[int(v4, base = 2)]:04b}"

                v2_star = xor(L1, y_star[4:8])
                v4_star = xor(L2, y_star[12:16])
                u2_star = f"{pi_s_reverse[int(v2_star,base = 2)]:04b}"
                u4_star = f"{pi_s_reverse[int(v4_star, base = 2)]:04b}"

                u2_dif = xor(u2, u2_star)
                u4_dif = xor(u4, u4_star)
                if u2_dif == "0110" and u4_dif == "0110":
                    key_candidate[(L1, L2)] += 1
            cur_time += 1
            if cur_time >= times:
                break

    max = -1
    maxkey = None
    for L1, L2 in key_candidate:
        if key_candidate[(L1, L2)] > max:
            max = key_candidate[(L1, L2)]
            maxkey = (L1, L2)
    return maxkey


def differential_attack(T_set, times, dif1=None, dif2=None, dif3=None, dif4=None):
    key_candidate = {}
    # for i in range(16):
    #     for j in range(16):
    #         key_candidate[(f"{i:04b}", f"{j:04b}")] = 0

    diffs = [dif1, dif2, dif3, dif4]
    active_diffs = [i for i, d in enumerate(diffs) if d is not None]
    num_active = len(active_diffs)
    for key in product(range(16), num_active):
        key_bin = tuple(f"{x:04b}" for x in key)
        key_candidate[key_bin] = 0

    cur_time = 0  # 有效次数....
    for (
        x,
        x_star,
        y,
        y_star,
    ) in T_set:  # Fixed: corrected unpacking order to match get_T_set
        if y[0:4] == y_star[0:4] and y[8:12] == y_star[8:12]:
            for L1, L2 in key_candidate:
                v2 = xor(L1, y[4:8])
                v4 = xor(L2, y[12:16])
                u2 = f"{pi_s_reverse[int(v2,base = 2)]:04b}"
                u4 = f"{pi_s_reverse[int(v4, base = 2)]:04b}"

                v2_star = xor(L1, y_star[4:8])
                v4_star = xor(L2, y_star[12:16])
                u2_star = f"{pi_s_reverse[int(v2_star,base = 2)]:04b}"
                u4_star = f"{pi_s_reverse[int(v4_star, base = 2)]:04b}"

                u2_dif = xor(u2, u2_star)
                u4_dif = xor(u4, u4_star)
                if u2_dif == "0110" and u4_dif == "0110":
                    key_candidate[(L1, L2)] += 1
            cur_time += 1
            if cur_time >= times:
                break

    max = -1
    maxkey = None
    for L1, L2 in key_candidate:
        if key_candidate[(L1, L2)] > max:
            max = key_candidate[(L1, L2)]
            maxkey = (L1, L2)
    return maxkey


K = 0b0011_1010_1001_0100_1101_0110_0011_1111
f"{0b0011_1010_1001_0100_1101_0110_0011_1111:032b}"
K = [int(num) for num in f"{0b0011_1010_1001_0100_1101_0110_0011_1111:032b}"]


def solution(K, times):
    T_set_gen = get_T_set(get_differential(f"{0b0000_1011_0000_0000:016b}"), K)
    maxkey = differential_attack(T_set_gen, times)
    print(maxkey)


# times 是 有效的次数。。。。因为有效的其实不多。。。。。所以其实用得挺快的
solution(K, 200)
