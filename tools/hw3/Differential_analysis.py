from SPN_copy import spn
from itertools import product
from collections import defaultdict
from utils import is_dif_satisfy, get_differential, get_reverse_func

# 解包顺序要看看啊，这一回好歹是claude救了我，

# 这里，我们的 x 和 x* 的长度 是16， 2

K = f"{0b0011_1010_1001_0100_1101_0110_0011_1111:032b}"



def get_T_set(delta_x, K):
    """
    得到用来攻击的 差分为delta_x 的集合; 由于需要从明文得到密文，所以需要K。
    Args
        delta_x(str) :长度16
        K(str): 长度32
        
    Returns
        generator : 生成 (x, x_star, y, y_star)四元组
    """
    # cur_time = 0
    # 因为混乱的格式而进行一堆转换
    K_intlist = [int(num) for num in K]
    for x, x_star in get_differential(delta_x):
        x_intlist = [int(num) for num in x]
        x_star_intlist = [int(num) for num in x_star]
        y_intlist = spn(x_intlist, K_intlist)
        y_star_intlist = spn(x_star_intlist, K_intlist)
        y = "".join(map(str, y_intlist))
        y_star = "".join(map(str, y_star_intlist))
        # cur_time += 1
        # print("H",cur_time)
        yield (x, x_star, y, y_star)



def differential_attack(T_set, times, dif1=None, dif2=None, dif3=None, dif4=None, reverse_func = None):
    key_candidate = defaultdict(int) # 不存在的键的值，会初始化为0

    diffs = [dif1, dif2, dif3, dif4]
    active_indices = [i for i, d in enumerate(diffs) if d is not None]
    active_diffs = [diffs[i] for i in active_indices]
    
    cur_time = 0  # 有效次数....
    for _, _, y, y_star in T_set:  # Fixed: corrected unpacking order to match get_T_set
        # 过滤无效对
        is_effective = True
        for i, dif in enumerate(diffs):
            if dif == None and y[4*i:4*i+4] != y_star[4*i:4*i+4]:
                is_effective = False
                break
        if not is_effective:
            continue
        
        if reverse_func :
            y = reverse_func(y)
            y_star = reverse_func(y_star)
            
        y_block = [y[4*i:4*i+4] for i in active_indices]
        y_star_block = [y_star[4*i:4*i+4] for i in active_indices]
        for key in product(range(16), repeat=len(active_indices)):
            key_bin = tuple(f"{x:04b}" for x in key)
            if is_dif_satisfy(key_bin, y_block, y_star_block ,active_diffs):
                key_candidate[key_bin] += 1
            
        # 计数，T到一定大小就比较准确了，可以控制不要用那么多。
        cur_time +=1
        if cur_time >= times:
            break

    maxkey = max(key_candidate, key= key_candidate.get)
    return maxkey




K = f"{0b0011_1010_1001_0100_1101_0110_0011_1111:032b}"
def solution(K, times):
    
    ans_K = [None for i in range(8)]
    
    
    T_set_gen1 = get_T_set(f"{0b0000_1011_0000_0000:016b}", K)
    try_maxkey1 = differential_attack(T_set_gen1, times,dif2="0110", dif4="0110")
    ans_K[5],ans_K[7] = try_maxkey1
    # print(try_maxkey1)
    
    T_set_gen2 = get_T_set(f"{0b0000_1010_0000_0000:016b}", K)
    try_maxkey2 = differential_attack(T_set_gen2, times,dif1="0110", dif3="0110", dif4="0110")
    ans_K[4],ans_K[6],_ = try_maxkey2
    # print(try_maxkey2)
    
    # T_set_gen3 = get_T_set(f"{0b0000_1010_0000_0000:016b}", K)
    # try_maxkey3 = differential_attack(T_set_gen3, times,dif1="0110", dif3="0110", dif4="0110")
    # ans_K[],ans_K[],_ = try_maxkey3
    # print(try_maxkey3)
    
    # 拿到K4 ok
    # T_set_gen3 = get_T_set(f"{0b1010_0000_0000_0000:016b}", K)
    # try_maxkey3 = differential_attack(T_set_gen3, times,dif1 ="1000", dif3 = "1000", dif4= "1000" ,reverse_func=get_reverse_func(ans_K, 1))
    # ans_K[3], _, _ = try_maxkey3
    
    # # 拿到K3 ok
    # T_set_gen4 = get_T_set(f"{0b0000_1010_0000_0000:016b}", K)
    # try_maxkey4 = differential_attack(T_set_gen4, times,dif1="0100" ,reverse_func=get_reverse_func(ans_K, 2))
    # ans_K[2] = try_maxkey4
    
    # # 拿到K2
    # T_set_gen5 = get_T_set(f"{0b :016b}", K)
    # try_maxkey5 = differential_attack(T_set_gen5, times,dif1= ,reverse_func=get_reverse_func(ans_K, 3))
    # ans_K[1] = try_maxkey5
    
    # # 拿到K1
    # # T_set_gen6 = get_T_set(f"{0b :016b}", K)
    # # try_maxkey6 = differential_attack(T_set_gen5, times,dif1= ,reverse_func=get_reverse_func(ans_K, 3))
    # # ans_K[1] = try_maxkey6
    # # 最后一层手动推吧
    
    return ans_K


# times 是 有效的次数。。。。因为有效的其实不多。。。。。所以其实用得挺快的
solution(K, 400)
