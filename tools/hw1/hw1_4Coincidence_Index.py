from hw1_1frequency import count_letter_frequency
from typing import List
from utils import multiply_shifted, letter_probabilities



def coincidence_index(inputfile:str, m:int):
    text = ""
    # 更好的编程习惯是使用 if inputfile  或者 try except
    try:
        with open(inputfile,"r", encoding="utf-8") as file:
            text = file.read()
            # 变成连续的大写的字符串
            text = ''.join(char for char in text.upper() if char.isalpha())
            
            
    except FileNotFoundError:
        print(f"错误: 输入文件 '{inputfile}' 不存在。")
        return
    
    Ilist = []
    for i in range(0,m):
        temp = [text[j] for j in range(i, len(text), m)]
        temp = ''.join(temp)
        # print(f"Group {i}: {temp}")
        Ilist.append(temp)
    
    indexes =[]
    for i in range(0, m):
        freq_dict, substr_total_count = count_letter_frequency(Ilist[i])
        Ic = sum([value*(value -1)  for key, value in freq_dict.items()]) /(substr_total_count*(substr_total_count-1)) 
        indexes.append(Ic)
        # print(freq_dict)

    return indexes,Ilist


def Mg_compute(substrings:List[str], m:int, ):
    Mg = []
    for i in range(0, m):
        freq_dict, substr_total_count = count_letter_frequency(substrings[i])
        for i in range(0,26):
            target_letter = chr(ord('A') + i)
            if target_letter not in freq_dict:
                freq_dict[target_letter] = 0

        freq_dict = dict(sorted(freq_dict.items()))
        Mg_yi = []
        for g in range(0,26):
            # print(letter_probabilities)
            # print(freq_dict)
            result_dict = multiply_shifted(letter_probabilities, freq_dict, g)
            Mg_yi.append(sum(result_dict.values())/substr_total_count)
        Mg.append(Mg_yi)
    return Mg

def print_Mg_pretty(Mg:List[List[float]], m):
    for i in range(0, m):
        print(f"substring:{i}")
        for j in range(0, 26):
            print(f"{j}:{Mg[i][j]}", end=" ")
        print()


if __name__ == "__main__":
    m = 6 # 感觉是6，不然就是3
    indexes,substrings = coincidence_index("cryptograph.txt", m)
    print(indexes)
    Mg = Mg_compute(substrings, m)
    print_Mg_pretty(Mg, m)
    
