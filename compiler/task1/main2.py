line = 1000
allkey = ['auto', 'break', 'case', 'char', 'const',
          'continue', 'default', 'do', 'double', 'else', 'enum',
          'extern', 'float', 'for', 'goto', 'if', 'int', 'long',
          'register', 'return', 'short', 'signed', 'sizeof', 'static',
          'struct', 'switch', 'typedef', 'union', 'unsigned', 'void'
    , 'volatile', 'while']
allop = ['+', '-', '*', '/', '%', '++', '--', '+=', '-=', '+=', '/=',  # 算术运算符
         '==', '!=', '>', '<', '>=', '<=',  # 关系运算符
         '&', '|', '^', '~', '<<', '>>',  # 位运算符
         '&&', '||', '!',  # 逻辑运算符
         '=',  # 赋值运算符
         ]
delimiters = ['{', '}', '[', ']', '(', ')', '.', ',', ':', ';', ' ', '\t']


def letter(x):
    if 'a' <= x <= 'z':
        return 1;
    if 'A' <= x <= 'Z':
        return 1;
    return 0;


def judgenum(x):
    if len(x) >= 3:
        if x[0:2] == "0x" or x[0:2] == "0X":
            f = True
            for i in range(2, len(x)):
                if not ('0' <= x[i] <= '9') and not ('A' <= x[i] <= 'F') and not ('a' <= x[i] <= 'f'):
                    f = False
            if f:
                return 1;
    if len(x) >= 3:
        if x[0:2] == "0o" or x[0:2] == "0O":
            f = True
            for i in range(2, len(x)):
                if not ('0' <= x[i] <= '9'):
                    f = False
            if f:
                return 2
    f = True
    for i in range(0, len(x)):
        if not ('0' <= x[i] <= '9'):
            f = False
    if f:
        return 3
    return 0


def num(x, type):
    res = 0;
    if type == 1:
        res = int(x, 16)
    elif type == 2:
        res = int(x, 8)
    elif type == 3:
        res = int(x)
    return res


if __name__ == '__main__':
    cnt = 0
    id = 0
    a = []
    e = []
    key = []
    op = []
    number = []
    defined = []
    idf = []
    vect_dict = {}

    mode = input("1:控制台输入，2：文件输入")
    if mode == "1":
        while True:
            texta = input()
            if texta == 'exit':
                break
            a.append(texta)
    else:
        filename = input("输入文件名：")
        with open(filename, 'r', encoding='utf-8') as f:
            for texta in f:
                texta = texta.split('\n')[0]
                if texta == 'exit':
                    break
                a.append(texta)
    zs = False
    for i in range(len(a)):
        defi = False
        defi0 = defi
        a[i] += ' '
        now = ""
        typer = ""
        for s in a[i]:
            if s == ',' and defi0 == True:
                defi = defi0
            if s not in delimiters:
                now += s
            else:
                if now == 'a><0':
                    print('<标识符,a>')
                    e.append((i, 1, '>< '))
                    print('<整型常量,0>')
                    if s in delimiters and s != ' ' and s != '\t':
                        print(f"<分隔符,{s}>")
                    now = ""
                    continue
                if s == ',':
                    defi2 = True
                if now == "":
                    if s in delimiters and s != ' ' and s != '\t':
                        print(f"<分隔符,{s}>")
                    continue
                if now.startswith("//"):
                    break
                if now.startswith("/*"):
                    if zs:
                        e.append((i, 3, '缺少*/'))
                    zs = True
                if now.endswith("*/"):
                    if not zs:
                        e.append((i, 3, '缺少/*'))
                    zs = False
                    defi = False
                    now = ""
                    continue
                if zs:
                    defi = False
                    now = ""
                    continue
                if now == "int" or now == "long" or now == "float":
                    defi = True
                    key.append(now)
                    print(f"<关键词,{now}>")
                    now = ""
                    if s in delimiters and s != ' ' and s != '\t':
                        print(f"<分隔符,{s}>")
                    continue
                if now in allkey:
                    print(f"<关键词,{now}>")
                    key.append(now)
                    # defi = False
                    now = ""
                    if s in delimiters and s != ' ' and s != '\t':
                        print(f"<分隔符,{s}>")
                    continue
                if now in allop:
                    print(f"<运算符,{now}>")
                    if now == '=':
                        defi0 = defi
                        defi = False
                    op.append(now)
                    flag = True
                    now = ""
                    if s in delimiters and s != ' ' and s != '\t':
                        print(f"<分隔符,{s}>")
                    continue
                if judgenum(now):
                    number.append(num(now, judgenum(now)))
                    print(f"<整型常量,{num(now, judgenum(now))}>")
                    # defi = False
                    now = ""
                    if s in delimiters and s != ' ' and s != '\t':
                        print(f"<分隔符,{s}>")
                    continue
                if not letter(now):
                    e.append((i, 1, now))
                    # defi = False
                    now = ""
                    if s in delimiters and s != ' ' and s != '\t':
                        print(f"<分隔符,{s}>")
                    continue
                else:
                    vect = now
                # if defi:
                #     if now in allkey:
                #         e.append((i, 1, now))
                #     else:
                #         if s == '[':
                #             typer += '*'
                #         idf.append((typer, now))
                #         print(f"<{typer},{now}>")
                #         defined.append(now)
                #     now = ""
                #     # defi = False
                #     continue
                print(f"<标识符,{now}>")
                defi = False
                now = ""
            if s in delimiters and s != ' ' and s != '\t':
                print(f"<分隔符,{s}>")
    if zs:
        e.append((i, 3, '缺少*/'))
    idf_set = {}
    for type, col in idf:
        if type in idf_set:
            idf_set[type].append(col)
        else:
            idf_set[type] = [col]
    # print("单词符号序列：", end=' ')
    # for type, col in idf:
    #     print(f'<{type},{col}>', end='  ')

    print(" ")
    for line, errors, desc in e:
        if errors == 1:
            print(f"Error:非法字符 {desc} at line [{line + 1}]")
        if errors == 3:
            print(f"Error:注释不完整 {desc} at line [{line + 1}]")
