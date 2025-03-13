
def count_letter_frequency(text):
    """
    统计字符串中每个英文字母的出现次数（不区分大小写）及总字母数。
    
    Args:
        text (str): 输入的字符串
    
    Returns:
        tuple: (freq_dict, total_count) 包含字母频率字典和总字母数
    """
    # 转换为大写并去除非字母字符
    text = ''.join(char for char in text.upper() if char.isalpha())
    
    # 计算总字母数
    total_count = len(text)
    
    # 初始化字典存储字母频率
    freq_dict = {}
    
    # 统计每个字母出现次数
    for char in text:
        freq_dict[char] = freq_dict.get(char, 0) + 1
    
    return freq_dict, total_count

def count_word_frequency(text, word_list):
    """
    统计字符串中指定字符串列表中每个词的出现次数（不区分大小写）。
    
    Args:
        text (str): 输入的字符串
        word_list (list): 需要统计的字符串列表（如 ['TH', 'HE']）
    
    Returns:
        dict: 每个指定字符串及其出现次数的字典
    """
    # 转换为大写
    text = text.upper()
    
    # 初始化字典存储词频
    freq_dict = {}
    
    # 统计每个指定字符串出现次数
    for word in word_list:
        word_upper = word.upper()
        count = text.count(word_upper)
        if count > 0:
            freq_dict[word_upper] = count
    
    return freq_dict

def print_sorted_results(freq_dict, total_count, sort_by="alphabetical", filename=None):
    """
    按指定方式排序并将结果写入文件，包含频率占比。
    
    Args:
        freq_dict (dict): 频率字典
        total_count (int): 总字母数
        sort_by (str): 排序方式，'alphabetical'（按字母顺序）或 'frequency'（按词频降序）
        filename (str): 输出文件名，如果为 None 则打印到控制台
    """
    if sort_by == "alphabetical":
        sorted_items = sorted(freq_dict.items())
        sort_note = "Sorted by alphabetical order"
    elif sort_by == "frequency":
        sorted_items = sorted(freq_dict.items(), key=lambda x: (-x[1], x[0]))
        sort_note = "Sorted by frequency (descending)"
    else:
        print("无效的排序方式！请使用 'alphabetical' 或 'frequency'。")
        return

    if filename:
        # 写入文件
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{sort_note}\n")
            for key, value in sorted_items:
                percentage = (value / total_count) * 100  # 计算百分比
                f.write(f"{key}: {value} (占 {percentage:.2f}%)\n")
        print(f"结果已写入文件: {filename}")
    else:
        # 打印到控制台
        print(sort_note)
        for key, value in sorted_items:
            percentage = (value / total_count) * 100  # 计算百分比
            print(f"{key}: {value} (占 {percentage:.2f}%)")

# 示例使用
if __name__ == "__main__":
    # 示例字符串
    sample_text = """
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
    
    # 调用字母频率统计
    letter_freq, total_count = count_letter_frequency(sample_text)
    print("字母频率统计：")
    print("按字母顺序排序：")
    print_sorted_results(letter_freq, total_count, "alphabetical")
    print("\n按词频降序排序：")
    print_sorted_results(letter_freq, total_count, "frequency")
    
    # 定义需要统计的字符串列表
    word_list = ['TH', 'HE', 'EA', 'AT']
    word_freq = count_word_frequency(sample_text, word_list)
    print("\n指定字符串词频统计：")
    print("按字母顺序排序：")
    # print_sorted_results(word_freq, total_count, "alphabetical")
    print("\n按词频降序排序：")
    # print_sorted_results(word_freq, total_count, "frequency")
