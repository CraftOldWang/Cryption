# 如果是维吉尼亚密码的话，可以试试Kasiski
from typing import Optional


def count_segment_freq(text:str, seg_len:int):
    text = ''.join(char for char in text.upper() if char.isalpha())
    freq_dict = {}
    text_length = len(text)
    for i in range(0, text_length -seg_len+1):
        seg = text[i: i+seg_len]
        if seg not in freq_dict:
            count = 0
            position = []
            for j in range(i, text_length-seg_len+1):
                if seg == text[j:j+seg_len]:
                    count+=1
                    position.append(j)  # position 该字符串起始下标
            freq_dict[seg] = tuple((count, position))
    return freq_dict
    
def print_segment_count(freq_dict:dict, sort_by:str = "alphabetical", filename=None):
    if sort_by == "alphabetical":
        sorted_items = sorted(freq_dict.items())
        sort_note = "Sorted by alphabetical order"
    elif sort_by == "frequency":
        sorted_items = sorted(freq_dict.items(), key=lambda x: (-x[1][0], x[0]))
        sort_note = "Sorted by frequency (descending)"
    else:
        print("无效的排序方式！请使用 'alphabetical' 或 'frequency'。")
        return
    
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{sort_note}\n")
            for key, value in sorted_items:
                if value[0] >= 2:
                    f.write(f"{key}: {value}\n")
        print(f"结果已写入文件{filename}")
    else:
        print(f"{sort_note}\n")
        for key, value in sorted_items:
            print(f"{key}:{value}\n")
        
    

if __name__ == "__main__":
    # 示例字符串
    with open("cryptograph.txt","r", encoding="utf-8") as f:
        sample_text = f.read()
    
    seg_dict = count_segment_freq(sample_text, 5)
    print("seg 频率统计\n")
    print("按照频率降序：")
    print_segment_count(seg_dict, "frequency", "Kasiski_result.txt")
    
    
    
    