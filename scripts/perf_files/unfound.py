import os

# 获取当前目录
current_directory = os.getcwd()

# 遍历当前目录下所有文件名含有"a-"的文件
matching_files = [filename for filename in os.listdir(current_directory) if "hr-" in filename]

# 读取每个匹配文件的前100行并与b.txt中的关键字比对
for file_name in matching_files:
    file_path = os.path.join(current_directory, file_name)

    with open(file_path, 'r', encoding='utf-8') as file_a:
        lines_a = file_a.readlines()

    with open('names.txt', 'r', encoding='utf-8') as file_b:
        keywords = [line.strip().lower() for line in file_b.readlines()]

    # 遍历前100行
    for i, line_a in enumerate(lines_a[11:120]):
        line_a = line_a.strip().lower()

        # 检查每个关键字是否在当前行中出现
        keyword_found = any(keyword in line_a for keyword in keywords)

        # 如果当前行中没有任何关键字，则输出行号
        if not keyword_found:
            print(line_a)
            print(f"{file_name}: Line {i + 1}")
