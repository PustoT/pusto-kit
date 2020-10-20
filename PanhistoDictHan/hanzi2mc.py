import requests
from bs4 import BeautifulSoup
import re
import sqlite3

mapInitials = {}
mapSjep = {}
mapTongx = {}
mapHo = {}
mapFinals = {}

mapUntInit = {}
mapUntFin = {}
mapUntFinPoly = {}

#hanzi = input('Input hanzi')
hanzis = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

def mc_from_sqlite(hanzi):
    mcs, pus = [], []
    unicd = hanzi.encode("unicode_escape")
    unicd = str(unicd) # like b'\\u4e00'
    unicd = unicd[5:-1].upper()
    conn = sqlite3.connect('mcpdict.db')
    c = conn.cursor()
    cursor = c.execute("SELECT * FROM mcpdict WHERE unicode = ?", (unicd,))
    for row in cursor:
        # print("unicode = ", row[0])
        mcs += row[1].split(',')
        # print("mc = ", row[1])
        pus += row[2].split(',')
        # print("pu = ", row[2])
        # print("ct = ", row[3], "\n")
    conn.close()
    return mcs, pus

# imit https://github.com/MaigoAkisame/MCPDict/blob/master/src/maigosoft/mcpdict/Orthography.java
def mcp2detail(mc):
    
    # Replace apostrophes with zeros to make SQLite FTS happy
    mc.replace('\'', '0')
    
    # tone
    tone = 0
    lastch = mc[-1]
    if lastch == 'x': 
        tone = 1
        mc = mc[:-1]
    elif lastch == 'h':
        tone = 2
        mc = mc[:-1]
    elif lastch == 'd':
        tone = 2
    elif lastch == 'p':
        tone = 3
        mc = mc[:-1] + 'm'
    elif lastch == 't':
        tone = 3
        mc = mc[:-1] + 'n'
    elif lastch == 'k':
        tone = 3
        mc = mc[:-1] + 'ng'
        
    # split initial and final
    init, fin = '', ''
    extraJ = False
    p = mc.find('0')
    if p >= 0: # Abnormal syllables containing apostrophes
        init = mc[:p]
        fin = mc[p+1:]
        if init == 'i': init = ''
        if init not in mapInitials.keys(): return None
        if fin not in mapFinals.keys(): return None
    else:
        for i in range(3, -1, -1):
            if i <= len(mc) and mc[:i] in mapInitials.keys():
                init, fin = mc[:i], mc[i:]
                break
        if fin == '': return None
        
        # Extract extra "j" in syllables that look like 重紐A類
        if fin[0] == 'j':
            if len(fin) < 2: return None
            extraJ = True
            if fin[1] == 'i' or fin[1] == 'y':
                fin = fin[1:]
            else:
                fin = 'i' + fin[1:]
        
        # Recover omitted glide in final
        if init[-1] == 'r': # 只能拼二等或三等韻，二等韻省略介音r
            if fin[0] != 'i' and fin[0] != 'y':
                fin = 'r' + fin
        elif init[-1] == 'j': # 只能拼三等韻，省略介音i
            if fin[0] != 'i' and fin[0] != 'y':
                fin = 'i' + fin

    if fin not in mapFinals.keys(): return None
    
    # Distinguish 重韻
    if fin == 'ia': # 牙音声母爲戈韻，其餘爲麻韻
        if init in ["k", "kh", "g", "ng"]:
            fin = 'Ia'
    elif fin in ['ieng', 'yeng']: # 脣牙喉音声母直接接-ieng,-yeng者及莊組爲庚韻，其餘爲清韻
        if not extraJ and init in [
                "p", "ph", "b", "m",
                "k", "kh", "g", "ng",
                "h", "gh", "q", "",
                "cr", "chr", "zr", "sr", "zsr"]:
            fin = 'Ieng' if fin == 'ieng' else 'Yeng'
    elif fin == 'in': # 莊組声母爲臻韻，其餘爲眞韻
        if init in ["cr", "chr", "zr", "sr", "zsr"]:
            fin = 'In'
    elif fin == 'yn': # 脣牙喉音声母直接接-yn者爲眞韻，其餘爲諄韻
        if not extraJ and init in[
                "p", "ph", "b", "m",
                "k", "kh", "g", "ng",
                "h", "gh", "q", ""]:
            fin = 'Yn'
        
    # Resolve 重紐
    dryungNriux = ""
    if "支脂祭眞仙宵侵鹽".find(mapFinals[fin][0]) >= 0 and init in [
            "p", "ph", "b", "m",
            "k", "kh", "g", "ng",
            "h", "gh", "q", "", "j"]:
        dryungNriux = 'A' if extraJ or init == 'j' else 'B'
        
    # Render details
    mux = mapInitials[init]
    sjep  = mapSjep[fin]
    yonh = mapFinals[fin][0] if fin[-1] == 'd' else mapFinals[fin][tone]
    tongx = mapTongx[fin]
    ho = mapHo[fin]
    
    tone = 0 if fin[-1] == 'd' else tone
    tone = "平上去入"[tone]
    yonh_repre = mapFinals[fin][0]
    mc_repre = mc
    
    return mux, sjep, yonh, dryungNriux, tongx, ho, tone, yonh_repre, mc_repre

def mc_from_ytenx(hanzi):
    url = 'https://ytenx.org/zim?dzih=' + hanzi + '&dzyen=1&jtkb=1&jtkd=1&jtdt=1&jtgt=1'
    strhtml = requests.get(url)
    # print(strhtml.text)
    
    soup=BeautifulSoup(strhtml.text,'lxml')
    
    data = soup.select('body > div.container.container-main > div > div > p.yonh')
    
    str_data = str(data)
    res1 = ''.join(re.findall('[\u4e00-\u9fa5]',str_data))
    mux = res1[5]
    yonh = res1[4]
    nriux = ''
    tongx = res1[2]
    ho = res1[1]
    if yonh + 'A' in str_data:
        nriux = 'A'
    if yonh + 'B' in str_data:
        nriux = 'B'
        
    print(mux, yonh, nriux, tongx, ho)

def init_maps():
    with open('orthography_mc_initials.tsv', 'r', encoding = 'utf8') as f:
        lines = f.readlines()
        for line in lines:
            if line == None or line == '' or line[0] == '#':
                continue
            fields = line.strip().split("\t")
            if fields[0] == "_": fields[0] = ""
            mapInitials[fields[0]] = fields[1]
    with open('orthography_mc_finals.tsv', 'r', encoding = 'utf8') as f:
        lines = f.readlines()
        for line in lines:
            if line == None or line == '' or line[0] == '#':
                continue
            fields = line.strip().split("\t")
            mapSjep[fields[0]] = fields[1]
            mapTongx[fields[0]] = fields[2]
            mapHo[fields[0]] = fields[3]
            mapFinals[fields[0]] = fields[4]

def mc_to_unt(mux, yonh_repre, dryungNriux, tongx, ho, mc, tone, mc_repre):
    '''
    方案：声母用poly查，韵母需要按代表韵目、重纽、等、开合，并注意谆清蒸，
        查出音标，再加声调或改入声。因为有汉字，宜明繁简。
        繁简不同者：魚、齊、廢、眞、諄、刪、蕭、談、鹽、銜、嚴、東、鍾、陽、職；開
        注意，蒸合只有入声，按unt改以职为代表，体现为拼音文件第一列也是职。
    Returns
    -------
    None.

    '''
    unt = mapUntInit[mux]
    if mux in ['見', '谿', '羣', '疑', '曉', '匣'] and tongx == '一':
        if mux == '見': unt = 'q'
        elif mux == '谿': unt = 'qʰ'
        elif mux == '羣': unt = 'ɢ'
        elif mux == '疑': unt = 'ɴ'
        elif mux == '曉': unt = 'χ'
        elif mux == '匣': unt = 'ʁ'
    
    # change 韵目代表、呼 to simplified chinese
    tran2simp = {'魚':'鱼', '齊':'齐', '廢':'废', '眞':'真', '諄':'谆', 
                 '刪':'删', '蕭':'萧', '談':'谈', '鹽':'盐', '銜':'衔', 
                  '嚴':'严', '東':'东', '鍾':'钟', '陽':'阳', '職':'职', '開':'开',}
    if yonh_repre in tran2simp.keys(): yonh_repre = tran2simp[yonh_repre]
    if ho in tran2simp.keys(): ho = tran2simp[ho]
    
    if yonh_repre == '谆':
        if mux in ['知', '徹', '澄', '娘', '莊', '初', '崇', '生', '俟']:
            unt += 'ɻɥin'
        else:
            unt += 'ɥin'
    elif yonh_repre == '清':
        if mc.find('jeng') >= 0:
            unt += 'jɛɲ'
        elif mc.find('ieng') >= 0:
            unt += 'ɻjɛɲ'
        elif mc.find('jyeng') >= 0:
            unt += 'ɥɛɲ'
        elif mc.find('yeng') >= 0:
            unt += 'ɻɥɛɲ'
    elif yonh_repre == '蒸':
        if mux in ['精', '清', '從', '心', '邪', '章', '昌', '常', '書', '船', '日', '以']:
            unt += 'iŋ'
        else:
            unt += 'ɻiŋ'
    elif "支脂祭真仙宵侵盐".find(yonh_repre) >= 0: # 重纽对立者，由于 maigo 程序有一些韵目不区分重纽，但unt 区分，因此根据拼音定重纽
        if mc_repre.find('r') != -1:
            dryungNriux = 'B'
        else:
            dryungNriux = 'A'

        possible_names = [yonh_repre + dryungNriux, yonh_repre + dryungNriux + ho]
        for y in possible_names:
            if y in mapUntFin.keys(): 
                unt += mapUntFin[y]
                # print(mc_repre, ' wa mc_repre ', y)
                break
    else:
        if yonh_repre + dryungNriux + ho in mapUntFin.keys(): unt += mapUntFin[yonh_repre + dryungNriux + ho]
        elif yonh_repre + dryungNriux in mapUntFin.keys(): unt += mapUntFin[yonh_repre + dryungNriux]
        elif yonh_repre + tongx + ho in mapUntFin.keys(): unt += mapUntFin[yonh_repre + tongx + ho]
        elif yonh_repre + tongx in mapUntFin.keys(): unt += mapUntFin[yonh_repre + tongx]
        elif yonh_repre + ho in mapUntFin.keys(): unt += mapUntFin[yonh_repre + ho]
        elif yonh_repre in mapUntFin.keys(): unt += mapUntFin[yonh_repre]
    
    chieng_muxs = ['幫', '端', '知', '精', '莊', '章', '見', '心', '生', '書', '曉', '影',
                   '滂', '透', '徹', '清', '初', '昌', '谿']
    zyen_druk =   ['並', '定', '澄', '從', '崇', '常', '羣', '邪', '俟', '船', '匣']
    chiih_druk =  ['明', '泥', '娘',             '日', '疑', '來', '云', '以']
    if tone == '平':
        if mux in chieng_muxs: unt += '˦'
        else: unt += '˨˩'
    elif tone == '上':
        if mux in chieng_muxs or mux in chiih_druk: unt += '˦˦˥'
        else: unt += '˨˨˧'
    elif tone == '去':
        if mux in chieng_muxs: unt += '˥˩'
        else: unt += '˧˩˨'
    else:
        if unt.endswith('m'): unt = unt[:-1] + 'p'
        elif unt.endswith('n'): unt = unt[:-1] + 't'
        elif unt.endswith('ɲ'): unt = unt[:-1] + 'c'
        elif unt.endswith('ŋ'): unt = unt[:-1] + 'k'
        elif unt.endswith('ŋʷ'): unt = unt.replace('ŋʷ', 'kʷ')
        if mux in chieng_muxs or mux in chiih_druk: unt += '˥'
        else: unt += '˨˩'
    return unt
        

def init_unt_maps():
    with open('unt_mc_initials.tsv', 'r', encoding = 'utf8') as f:
        lines = f.readlines()
        for line in lines:
            if line == None or line == '' or line[0] == '#':
                continue
            fields = line.strip().split("\t")
            if fields[2] == "_": fields[2] = ""
            mapUntInit[fields[1]] = fields[2]
    with open('unt_mc_finals.tsv', 'r', encoding = 'utf8') as f:
        lines = f.readlines()
        for line in lines:
            if line == None or line == '' or line[0] == '#':
                continue
            fields = line.strip().split("\t")
            mapUntFin[fields[2]] = fields[3]
            mapUntFinPoly[fields[2]] = fields[5]

init_maps()
init_unt_maps()

def hanzis2mcinfos(hanzis):
    res = ''
    for hanzi in hanzis:
        res += '\n' + hanzi
        print('\n' + hanzi)
        mcs, pus = mc_from_sqlite(hanzi)
        res += ','.join(pus)
        print(','.join(pus))
        for mc in mcs:
            mux, sjep, yonh, dryungNriux, tongx, ho, tone, yonh_repre, mc_repre = mcp2detail(mc)
            res += mux + sjep + yonh + dryungNriux + tongx + ho + ' ' + tone + yonh_repre
            print(mux + sjep + yonh + dryungNriux + tongx + ho + ' ' + tone + yonh_repre)
            unt = mc_to_unt(mux, yonh_repre, dryungNriux, tongx, ho, mc, tone, mc_repre)
            res += unt
            print(unt)
    
    return res

