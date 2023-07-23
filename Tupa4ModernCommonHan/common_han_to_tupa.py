m = {}
with open("./tupa.dict.yaml", 'r', newline='') as reader:
    for l in reader.readlines():
        han, tupa = l.split()[0], l.split()[1]
        if len(han) == 1:
            m[han] = m.get(han, []) + [tupa]
#print(m)
res_han_tupa = {}
with open("./hanzi.txt", 'r', newline='') as reader:
    for l in reader.readlines():
        han = l.strip()
        res_han_tupa.update({han: m.get(han, [])})
        if han not in m:
            print("！！！！！！此字不存在于tupa表" + han)
# print(res_han_tupa)

with open("./result_hanzi_tupa.txt", 'w', newline='') as writer:
    for han, tupas in res_han_tupa.items():
        writer.write(han + '\t' + str(tupas) + '\n')

res_tupa_han = {}
for han, tupas in res_han_tupa.items():
    for tupa in tupas:
        res_tupa_han[tupa] = res_tupa_han.get(tupa, []) + [han]
print(res_tupa_han)

with open("./result_tupa_hanzi.txt", 'w', newline='') as writer:
    for tupa, hans in res_tupa_han.items():
        writer.write(tupa + '\t' + str(hans) + '\n')

max_cnt_pronunciations = max([len(v) for v in res_han_tupa.values()])
print(max_cnt_pronunciations)
for han, tupas in res_han_tupa.items():
    if len(tupas) == max_cnt_pronunciations:
        print(han + '\t' + str(tupas))

max_cnt_homophones = max([len(v) for v in res_tupa_han.values()])
print(max_cnt_homophones)
for tupa, hans in res_tupa_han.items():
    if len(hans) == max_cnt_homophones:
        print(tupa + '\t' + str(hans))
