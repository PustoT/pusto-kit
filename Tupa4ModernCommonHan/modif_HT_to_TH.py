# 从修改后的 hanzi tupa 文件构建 hanzi -> tupa 的映射，忽略井号后的注释内容
res_han_tupa = {}
with open("./modified_hanzi_tupa.yaml", 'r', newline='') as reader:
    for line in reader:
        # 忽略井号后的内容
        line = line.split('#')[0].strip()
        if not line:
            continue  # 如果该行只有注释或为空，跳过

        parts = line.split('\t')
        if len(parts) == 2:
            han, tupas = parts[0], eval(parts[1])  # eval用于解析字符串形式的列表
            res_han_tupa[han] = tupas

# 根据 res_han_tupa 构建 tupa -> hanzi 的映射
res_tupa_han = {}
for han, tupas in res_han_tupa.items():
    for tupa in tupas:
        res_tupa_han[tupa] = res_tupa_han.get(tupa, []) + [han]

# 将 res_tupa_han 按 value 长度从大到小排序
sorted_res_tupa_han = dict(sorted(res_tupa_han.items(), key=lambda x: len(x[1]), reverse=True))

# 将排序后的 tupa -> hanzi 映射写入新的文件，并以井号分隔每行的注释
with open("./modified_tupa_hanzi.yaml", 'w', newline='') as writer:
    for tupa, hans in sorted_res_tupa_han.items():
        writer.write(f"{tupa}\t{str(hans)}\n")  # 如果需要注释，可以在此行加上 # 后的内容
