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
    entries = mc_from_sqlite(hanzi)
    trues = entries[lang2n[target_lang] - 1]
    mcs = entries[0]
    return ans in trues, trues, mcs

common_hanzis = []
with open("./common-hanzi.txt", 'r', newline='') as reader:
    for l in reader.readlines():
        han = l.strip()
        common_hanzis.append(han)

print(mc_from_sqlite('阱'))

target_lang = input('What to learn (mc, pu, yue, wuu, nan): ')

isRandomMode = False
while True:
    print('\n')
    hanzi = ''
    if not isRandomMode:
        hanzi = input('輸入漢字或「exit」 Input a 漢字 hanzi or "exit", \n或留白以（全程）隨機 or blank for random hanzi (the entire session): ')
    if hanzi == 'exit':
        break
    elif hanzi == '':
        isRandomMode = True
        hanzi = random.choice(common_hanzis)
        print('請回答此隨機漢字 Answer this random han: ', hanzi)
        print("\033[1;33m" + "(*´･д･)? " + hanzi + "\033[0m")
    
    print('Input your answer: ')
    ans = input('>> ')

    if ans == 'exit':
        isRandomMode = False
        continue

    res, trues, mcs = verify_ans(target_lang, hanzi, ans)
    if res == True:
        print("\033[1;32m" + '(♥ω♥*) Correct! The answers are ' + str(trues) + "\033[0m")
        print('The Middle Chinese KYonhs are: ', mcs)
    else:
        print("\033[1;31m" + '(°ω°) False! The answer should be: ' + str(trues) + "\033[0m")
        print('The Middle Chinese KYonhs are: ', mcs)
    # TODO: remind the Middle Chinese information
