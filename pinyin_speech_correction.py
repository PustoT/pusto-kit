# 将拼音方案的拼音处理为方便语音分析的改版拼音；提供将改版拼音转换为标准拼音的接口；
# 用规则由原拼音生成多个与之相似的拼音，即模糊匹配；每个原拼音串生成多个模糊匹配拼音串，进而生成对应的可能的汉字串；
# 汉字串列表在数据库中检索，给每个匹配的加上频率，删除无匹配的；
# 韵母表如下，由于数量有限，模糊规则中对介音、韵腹、韵尾不分开处理。
# a, o, e, ai, ei, ao, ou, an, en, ang, eng
# i, u, v, ia, ua, uo, ie, ve, uai, ui, iao, iu, ian, uan, van, in, un, vn, iang, uang, ing, iong, ong
# y、w 处理为零声母：yu - v, y - i, w - u
# ueng 与 ong 互补，仅在零声母出现，统一使用 ong

# exemple dusage
"""
from pinyin_speech_correction import pinyins2fuzzies
csv_pinyin_str = "['wu4', 'xing2', 'gan1', 'yan2']"
pinyins = eval(csv_pinyin_str)
hanzi_seqs = pinyins2fuzzies(pinyins)
"""

def devide_pinyin(orig):
    """
    devide a pinyin to get 声母、韵母（不分介音、韵腹、韵尾）
    """
    sheng, yun, diao = "", "", ""

    # get 声母
    if orig[0] in ["a", "i", "u", "e", "o", "v", "y", "w"]: # 零声母
        sheng = ""
        # 汉语拼音方案特殊声母 y、w 音素化
        if orig[0] == "y": 
            if orig[1] == "i":
                orig = "i" + orig[2:]
            elif orig[1] == "u":
                orig = "v" + orig[2:]
            elif orig[1:] == "ou":
                orig = "iu"
            else:
                orig = "i" + orig[1:]
        elif orig[0] == "w":
            if orig[1] == "u":
                orig = "u" + orig[2:]
            elif orig[1:] == "en":
                orig = "un"
            elif orig[1:] == "eng":
                orig = "ong"
            elif orig[1:] == "ei":
                orig = "ui"
            else:
                orig = "u" + orig[1:]
    elif orig[0] in ["z", "c", "s"] and orig[1] is "h": # 翘舌音
        sheng = orig[0:2]
        orig = orig[2:]
    elif orig[0] in ["j", "q", "x"] and orig[1] == "u": # j q x + u = + v
        sheng = orig[0]
        orig = "v" + orig[2:]
    else:
        sheng = orig[0]
        orig = orig[1:]

    # get 韵母, and tone, if the last char is digit
    if orig[-1].isdigit():
        yun = orig[:-1]
        diao = orig[-1]
    else:
        yun = orig
        diao = ""
    return sheng, yun, diao

def build_pinyin(sheng, yun, diao = ""):
    res = ""
    # use y, w for some of those without shengmu
    ius = ["i",  "in",  "ing",  "iu",  "un",  "ong",  "ui",  "u"]
    yws = ["yi", "yin", "ying", "you", "wen", "weng", "wei", "wu"]
    if sheng == "" :
        if yun in ius:
            res = yws[ius.index(yun)]
        elif yun[0] == "i":
            res = "y" + yun[1:]
        elif yun[0] == "v":
            res = "yu" + yun[1:]
        elif yun[0] == "u":
            res = "w" + yun[1:]
        else:
            res = yun
        
    # jqx + v = u
    elif sheng in ["j", "q", "x"] and yun[0] == "v":
        res = sheng + "u" + yun[1:]

    else:
        res = sheng + yun

    return res

def fuzzy_pinyins(orig):
    """
    construct a list of pinyin strings based on one, for fuzzy matching
    paras:
        orig: origin
    returns:
        res: result
    """
    # 替代：声调、平翘舌、前后鼻音、n-l、hu*-fu*、送气不送气、介音混淆（齐齿-撮口、开口-合口）
    # （替代之暂未开启：b-m, n-y（蜗牛-我有））
    # （暂未开启）（插入/删除：介音、韵尾、某些声母、零声母（西安仙））

    temp, res = [ ], [ ]
    sheng, yun, diao = "", "", ""

    # 若是拉丁字母，小处理
    latin2pinyin = {"A":("", "ei"), "B":("b", "i"),  "C":("s", "ei"),  "D":("d", "i"),
                    "E":("", "i"),  "G":("j", "i"),  "J":("zh", "ei"), "K":("k", "ei"),
                    "N":("", "en"), "Q":("q", "iu"), "R":("", "a"),    "U":("", "iu"),
                    "V":("", "ui"), "Y":("", "uai"), "Z":("z", "ei")}
    if  len(orig) == 1:
        if orig.upper() in latin2pinyin.keys():
            sheng, yun = latin2pinyin[orig.upper()]
        else:
            sheng, yun = "", "ai"
    else:
        # 正常汉语拼音往下走
        sheng, yun, diao = devide_pinyin(orig)
    
    temp.append((sheng, yun))

    # 平翘舌
    if sheng in ["z", "c", "s"]:
        temp.append((sheng + "h", yun))
    elif sheng in ["zh", "ch", "sh"]:
        temp.append((sheng[0], yun))
    
    # 前后鼻音
    _n =  ["an",  "en",  "in",  "ian",  "uan",  "un"]
    _ng = ["ang", "eng", "ing", "iang", "uang", "ong"]
    if yun in _n:
        temp.append((sheng, _ng[_n.index(yun)]))
    elif yun in _ng:
        temp.append((sheng, _n[_ng.index(yun)]))
    
    # n-1
    if sheng == "n":
        temp.append(("l", yun))
    elif sheng == "l":
        temp.append(("n", yun))
    
    # hu*-fu*
    hu = [("h", "u"), ("h", "un"), ("h", "ui"), ("h", "ong"), 
            ("h", "uan"), ("h", "uang"), ("h", "uo"), ("h", "ua")] # , ("h", "uai")
    fu = [("f", "u"), ("f", "en"), ("f", "ei"), ("f", "eng"), 
            ("f", "an"),  ("f", "ang"),  ("f", "o"),  ("f", "a")] # , ("f", "ai")
    if sheng == "h" and (sheng, yun) in hu:
        temp.append(fu[hu.index((sheng, yun))]) 
    elif sheng == "f" and (sheng, yun) in fu:
        temp.append(hu[fu.index((sheng, yun))]) 

    # 送气-不送气
    asp = ["p", "t", "k", "q", "ch", "c"]
    unasp = ["b", "d", "g", "j", "zh", "z"]
    if sheng in asp:
        temp.append((unasp[asp.index(sheng)], yun))
    elif sheng in unasp:
        temp.append((asp[unasp.index(sheng)], yun))

    # 齐齿呼-撮口呼 i-v, ie-ve, ian-van, in-vn
    i = ["i", "ie", "ian", "in"]
    v = ["v", "ve", "van", "vn"]
    if yun in i:
        temp.append((sheng, v[i.index(yun)]))
    elif yun in v:
        temp.append((sheng, i[v.index(yun)]))

    # 开口呼-合口呼 ["an", "ang", "o", "ang", "a", "ai"] -> "u"+, en-un, ei-ui, eng-ong (此不虑零声母) 
    aa = ["an",  "ang",  "o",  "ang",  "a",  "ai",
            "en", "ei", "eng"]
    ua = ["uan", "uang", "uo", "uang", "ua", "uai",
            "un", "ui", "ong"]
    if yun in aa:
        temp.append((sheng, ua[aa.index(yun)]))
    elif yun in ua:
        temp.append((sheng, aa[ua.index(yun)]))

    print(temp)

    # give 4 tones to every items in temp
    for t in temp:
        s = build_pinyin(t[0], t[1])
        res.append(s)
        # to use Py2Hz, no is here tone number
        # res.append(s + "1")
        # res.append(s + "2")
        # res.append(s + "3")
        # res.append(s + "4")

    return res

from Pinyin2Hanzi import simplify_pinyin, is_pinyin, DefaultDagParams, dag

def pinyins2fuzzies(pinyins):
    """
    para:   pinyins: List of str of pinyin, like ['jia3', 'zhuang4', 'xian4', 'nang2', 'zhong3']
    return: res: List of str of possible Hanzi seq
    """

    # 每个原拼音造新拼音，化为Py2Hz的标准格式，保留合法者。由是，第一维字，第二维假拼
    char_py_list = []
    for orig_py in pinyins:
        char_py_list.append([])
        tmp = fuzzy_pinyins(orig_py)
        for new_py in tmp:
            if is_pinyin(simplify_pinyin(new_py)):
                char_py_list[-1].append(simplify_pinyin(new_py))    

    # py表组合成很多拼音串
    p, q = [], []
    p = [ [i] for i in char_py_list[0]]
    for ch in char_py_list[1:]: # 每个汉字位都多一波组合
        for i in p: # 已处理列表中的每个元素，与每个新位置元素结合
            for j in ch:
                q.append(i + [j])
        p = q
        q = []
    pinyin_seqs = p
        
    res = []
    # 每个拼音串用dag化为句子
    dagparams = DefaultDagParams()
    for seq in pinyin_seqs:
        hanzi_seqs = dag(dagparams, tuple(seq), path_num=10)
        for hanzi_seq in hanzi_seqs:
            res.append(''.join(hanzi_seq.path))

    return res
