import ast  # 用于安全解析字符串形式的元组和列表
from tools.utils import parse_and_gcd

def count_diff_then_gcd(input_file, output_file):
    """
    从输入文件中读取频率数据，筛选频率 >= 2 的子串，计算下标差值，写入输出文件。
    
    参数:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    # 读取文件并解析数据
    freq_dict = {}
    try:
        with open(input_file, "r", encoding="utf-8") as infile:
            for line in infile:
                line = line.strip()  # 去掉首尾空白
                if line:  # 跳过空行
                    try:
                        # 分割键和值，例如 "AHT: (2, [131, 185])"
                        key, value_str = line.split(": ", 1)
                        # 安全解析字符串形式的元组，例如 "(2, [131, 185])"
                        value = ast.literal_eval(value_str)
                        freq_dict[key] = value
                    except (ValueError, SyntaxError) as e:
                        print(f"解析错误，跳过行: {line} ({e})")
    except FileNotFoundError:
        print(f"错误: 输入文件 '{input_file}' 不存在。")
        return

    # 筛选频率大于等于 2 的子串
    filtered_items = {key: value for key, value in freq_dict.items() if value[0] >= 2}
    
    # 写入结果到输出文件
    with open(output_file, "w", encoding="utf-8") as outfile:
        if not filtered_items:
            outfile.write("没有频率大于等于 2 的子串。\n")
        else:
            outfile.write("频率大于等于 2 的子串及其下标差值:\n")
            for seg, (count, positions) in filtered_items.items():
                if len(positions) > 1:  # 确保至少有两个下标
                    diffs = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
                    outfile.write(f"{seg}: count={count}, positions={positions}, diffs={diffs}\n")
                else:
                    outfile.write(f"{seg}: count={count}, positions={positions}, diffs=[] (不足两个下标)\n")

def append_gcd_result(input_file, output_file):
    text = ""
    with open(input_file, "r", encoding="utf-8") as file:
        text = file.read()
    gcd_result = parse_and_gcd(text)
    with open(output_file, "a", encoding="utf-8") as file:
        file.write(f"GCD: {gcd_result}\n")

    
    
# 示例调用
if __name__ == "__main__":
    input_file = "Kasiski_result.txt"
    output_file = "diff.txt"
    count_diff_then_gcd(input_file, output_file)
    print(f"处理完成，结果已写入 '{output_file}'。")
    append_gcd_result(output_file,output_file)