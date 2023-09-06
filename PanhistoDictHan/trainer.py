import sqlite3
import re
import random

hanzis = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

def mc_from_sqlite(hanzi):
    mcs, pus, yues, wuus, nans = [], [], [], [], []
    unicd = hanzi.encode("unicode_escape")
    unicd = str(unicd) # like b'\\u4e00'
    unicd = unicd[5:-1].upper()
    conn = sqlite3.connect('mcpdict.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM mcpdict WHERE unicode = ?", (unicd,))
    for row in cursor:
        # print("unicode = ", row[0])
        if row[1]: mcs += row[1].split(',')
        # print("mc = ", row[1])
        if row[2]: pus += row[2].split(',')
        # print("pu = ", row[2])
        # print("ct = ", row[3], "\n")
        if row[3]: yues += re.split('[,\(\)\[\]\*]', row[3]) # 训练模式拆开异读故()亦拆。否则不建议。
        if row[4]: wuus += row[4].split(',')
        if row[5]: nans += re.split('[,\(\)\[\]\*]', row[5])
    conn.close()
    return mcs, pus, yues, wuus, nans

def verify_ans(target_lang, hanzi, ans):
    lang2n = {'mc': 1, 'pu': 2, 'yue': 3, 'wuu': 4, 'nan': 5}
    trues = mc_from_sqlite(hanzi)[lang2n[target_lang] - 1]
    return ans in trues, trues

common_hanzis = []
with open("./common-hanzi.txt", 'r', newline='') as reader:
    for l in reader.readlines():
        han = l.strip()
        common_hanzis.append(han)

print(mc_from_sqlite('阱'))

target_lang = input('What to learn (mc, pu, yue, wuu, nan): ')

while True:

    hanzi = input('Input a 漢字 hanzi or "exit", or blank for random hanzi: ')
    if hanzi == 'exit':
        break
    elif hanzi == '':
        hanzi = random.choice(common_hanzis)
        print('Your random han is ', hanzi)
    ans = input('Input your answer: ')
    res, trues = verify_ans(target_lang, hanzi, ans)
    if res == True:
        print('＜（＾－＾）＞ Correct!')
    else:
        print('xxxxx False! The answer should be: ', trues)
    # TODO: remind the Middle Chinese information
