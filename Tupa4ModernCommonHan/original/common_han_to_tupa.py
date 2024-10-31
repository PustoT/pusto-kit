m = {}
with open("./tupa.dict.yaml", 'r', newline='') as reader:
    for l in reader.readlines():
        han, tupa = l.split()[0], l.split()[1]
        if len(han) == 1:
            m[han] = m.get(han, []) + [tupa]

# 构建 res_han_tupa 字典
res_han_tupa = {}
with open("./hanzi.txt", 'r', newline='') as reader:
    for l in reader.readlines():
        han = l.strip()
        res_han_tupa.update({han: m.get(han, [])})
        if han not in m:
            print("！！！！！！此字不存在于tupa表" + han)

# 将 res_han_tupa 按 value 长度从大到小排序
sorted_res_han_tupa = dict(sorted(res_han_tupa.items(), key=lambda x: len(x[1]), reverse=True))

with open("./sorted_result_hanzi_tupa.txt", 'w', newline='') as writer:
    for han, tupas in sorted_res_han_tupa.items():
        writer.write(han + '\t' + str(tupas) + '\n')

# 构建 res_tupa_han 字典
res_tupa_han = {}
for han, tupas in res_han_tupa.items():
    for tupa in tupas:
        res_tupa_han[tupa] = res_tupa_han.get(tupa, []) + [han]

# 将 res_tupa_han 按 value 长度从大到小排序
sorted_res_tupa_han = dict(sorted(res_tupa_han.items(), key=lambda x: len(x[1]), reverse=True))

with open("./sorted_result_tupa_hanzi.txt", 'w', newline='') as writer:
    for tupa, hans in sorted_res_tupa_han.items():
        writer.write(tupa + '\t' + str(hans) + '\n')

# 输出最多发音数的汉字及对应发音数
max_cnt_pronunciations = max([len(v) for v in res_han_tupa.values()])
print(max_cnt_pronunciations)
for han, tupas in res_han_tupa.items():
    if len(tupas) == max_cnt_pronunciations:
        print(han + '\t' + str(tupas))

# 输出最多同音字数的拼音及对应汉字数
max_cnt_homophones = max([len(v) for v in res_tupa_han.values()])
print(max_cnt_homophones)
for tupa, hans in res_tupa_han.items():
    if len(hans) == max_cnt_homophones:
        print(tupa + '\t' + str(hans))
