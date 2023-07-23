m = {}
with open("./tupa.dict.yaml", 'r', newline='') as reader:
    for l in reader.readlines():
        han, tupa = l.split()[0], l.split()[1]
        if len(han) == 1:
            m[han] = m.get(han, []) + [tupa]
#print(m)
res = {}
with open("./hanzi.txt", 'r', newline='') as reader:
    for l in reader.readlines():
        han = l.strip()
        res.update({han: m.get(han, [])})
        if han not in m:
            print("！！！！！！此字不存在于tupa表" + han)
print(res)

# with open("./result_hanzi_tupa.txt", 'w', newline='') as writer: