# 需要两个映射，
# pi S :  把l 长度 里面的，根据位置进行交换
# pi P ： 整个里面， 把某个数换成另一个


# 需要bit序列。。。或者直接用列表，存K， Kr用切片来算....或者弄一个二倍长度的，这样模完不会超
# 明文 。。。 16，  l(分组长度在这个里面作用pi s) = m(组数) = Nr(加密轮数) = 4
# TODO 写完了解一下白化是什么。。。
l = m = Nr = 4

# 其实这个用列表就可以了，毕竟下标嘛
pi_s = {
    0: 14,
    1: 4,
    2: 13,
    3: 1,
    4: 2,
    5: 15,
    6: 11,
    7: 8,
    8: 3,
    9: 10,
    10: 6,
    11: 12,
    12: 5,
    13: 9,
    14: 0,
    15: 7,
}

pi_p = {
    0: 1,
    1: 5,
    2: 9,
    3: 13,
    4: 2,
    5: 6,
    6: 10,
    7: 14,
    8: 3,
    9: 7,
    10: 11,
    11: 15,
    12: 4,
    13: 8,
    14: 12,
    15: 16,
}


def get_Kr(r, K):
    K = K * 2
    # 为了取每个K_r 方便点  # 这个K ， 应该不会该全局变量吧？或者说 *= 会改变吗,创建了一个新列表
    index = 4 * r - 3 - 1
    index = index % 32
    return K[index : index + 16]


def xor(a: list, b: list):
    return [0 if a[i] == b[i] else 1 for i in range(len(a))]


def do_substitute(u: list):  # l = m = 4 ; l 分组长度；m 组数
    v = []
    for i in range(m):
        tmp = u[4 * i : 4 * i + l]
        before_pi_s = int("".join(str(tmp[i]) for i in range(4)), base=2)
        after_pi_s = pi_s[before_pi_s]  # 应该不会出事的...
        v.extend(list(format(after_pi_s,"04b")))
    return [int(item) for item in v]


def do_permutation(v: list):
    res = [None] * l * m
    for i in range(l * m):
        res[pi_p[i] - 1] = v[i]
    return res


# x = list(map(int, [int(num) for num in str(input())] ))
# x = list(map(int, input()))  # 也是。。。直接读取一行
# x = [int(num) for num in input()] # 由于是直接读取一行，所以可以这么搞 ,且读出来字符串是iterable
K = list(map(int, input()))
# x = a_bits
# K = b_bits


def spn(x:list,K:list):
    """
    Args
        x(list): 明文，以01整数列表的形式
        K(list): 密钥，以01整数列表的形式
    Return
        y(list): 密文， 以01整数列表的形式
    """
    if type(x) == type(K) and type(x) == str:
        x = [int(num) for num in x]
        K = [int(num) for num in K]
    w = x
    for r in range(1, Nr):
        u = xor(w, get_Kr(r, K))
        v = do_substitute(u) 
        w = do_permutation(v)
    u = xor(w, get_Kr(Nr, K))
    v = do_substitute(u)
    y = xor(v, get_Kr(Nr + 1, K))
    # for i in range(l*m):
    #     print(y[i],end = "")
    return y  # 长度为 l*m= 4*4 = 16 的list...
    