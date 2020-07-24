# 韵母表如下，由于数量有限，模糊规则中对介音、韵腹、韵尾不分开处理。
# a, o, e, ai, ei, ao, ou, an, en, ang, eng
# i, u, v, ia, ua, uo, ie, ve, uai, ui, iao, iu, ian, uan, van, in, un, vn, iang, uang, ing, ueng, iong, ong
# y、w 处理为零声母：yu - v, y - i, w - u

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
            elif orig[1:3] == "ou":
                orig = "iu"
            else:
                orig = "i" + orig[1:]
        elif orig[0] == "w":
            if orig[1] == "u":
                orig = "u" + orig[2:]
            elif orig[1:] == "en":
                orig = "un"
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
    if sheng == "" :
        if yun in ["i", "in", "ing"]:
            res = "y" + yun
        elif yun == "iu":
            res = "you"
        elif yun[0] == "i":
            res = "y" + yun[1:]
        elif yun[0] == "v":
            res = "yu" + yun[1:]
        elif yun == "un":
            res = "wen"
        elif yun == "ueng" or yun == "ong":
            res = "weng"
        elif yun == "ui":
            res = "wei"
        elif yun == "u":
            res = "wu"
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
    if  len(orig) == 1:
        if orig.upper() == "A":
            yun = "ei"
        elif orig.upper() == "B":
            sheng, yun = "b", "i"
        elif orig.upper() == "C":
            sheng, yun = "s", "ei"
        elif orig.upper() == "D":
            sheng, yun = "d", "i"
        elif orig.upper() == "E":
            sheng, yun = "", "i"
        elif orig.upper() == "G":
            sheng, yun = "j", "i"
        elif orig.upper() == "J":
            sheng, yun = "zh", "ei"
        elif orig.upper() == "K":
            sheng, yun = "k", "ei"
        elif orig.upper() == "N":
            sheng, yun = "", "en"
        elif orig.upper() == "Q":
            sheng, yun = "q", "iu"
        elif orig.upper() == "R":
            sheng, yun = "", "a"
        elif orig.upper() == "U":
            sheng, yun = "", "iu"    
        elif orig.upper() == "V":
            sheng, yun = "", "ui"
        elif orig.upper() == "Y":
            sheng, yun = "", "uai"
        elif orig.upper() == "Z":
            sheng, yun = "z", "ei"
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
    if yun in ["an", "en", "in", "ian", "uan"]:
        temp.append((sheng, yun + "g"))
    elif yun == "un":
        temp.append((sheng, "ueng"))
    elif yun in ["ang", "eng", "ing", "iang", "uang"]:
        temp.append((sheng, yun[:-1]))
    elif yun == "ueng":
        temp.append((sheng, "un")) 
    
    # n-1
    if sheng == "n":
        temp.append(("l", yun))
    elif sheng == "l":
        temp.append(("n", yun))
    
    # hu*-fu*
    if sheng == "h":
        if yun == "u":
            temp.append(("f", "u"))
        elif yun == "un":
            temp.append(("f", "en"))
        elif yun == "ui":
            temp.append(("f", "ei"))
        elif yun[0] == "u":
            temp.append(("f", yun[1:])) 
        elif yun == "ong":
            temp.append(("f", "eng")) 
    elif sheng == "f":
        if yun == "u":
            temp.append(("h", "u"))
        elif yun == "en":
            temp.append(("h", "un"))
        elif yun == "ei":
            temp.append(("h", "ui"))
        elif yun in ["an", "ang", "o", "ang", "a", "ai"]:
            temp.append(("h", "u" + yun))
        elif yun == "eng":
            temp.append(("h", "ong"))

    # 送气-不送气
    #asp = ["p", "t", "k", "q", "ch", "c"]
    #unasp = ["b", "d", "g", "j", "zh", "z"]
    asp2unasp = {"p":"b", "t":"d", "k":"g", "q":"j", "ch":"zh", "c":"z"}
    unasp2asp = {"b":"p", "d":"t", "g":"k", "j":"q", "zh":"ch", "z":"c"}
    if sheng in ["p", "t", "k", "q", "ch", "c"]:
        temp.append((asp2unasp[sheng], yun))
    elif sheng in ["b", "d", "g", "j", "zh", "z"]:
        temp.append((unasp2asp[sheng], yun))

    # 齐齿呼-撮口呼 i-v, ie-ve, ian-van, in-vn
    i = ["i", "ie", "ian", "in"]
    v = ["v", "ve", "van", "vn"]
    if yun in i:
        temp.append((sheng, v[i.index(yun)]))
    elif yun in v:
        temp.append((sheng, i[v.index(yun)]))

    # 开口呼-合口呼 ["an", "ang", "o", "ang", "a", "ai"] -> "u"+, en-un, ei-ui, eng-ong (此不虑零声母) 
    aa = ["an", "ang", "o", "ang", "a", "ai",
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
