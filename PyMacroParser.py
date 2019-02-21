# -*- coding: UTF-8 -*-
class BufferReader:

    listIndex = 0
    bufferList = ["", ""]
    index = 0
    end = False
    cFile=None
    maxLength=10
    line=0

    def __init__(self,path):
        self.cFile=open(path,"r")
        self.bufferList[0]=self.cFile.read(self.maxLength)
        self.bufferList[1]=self.cFile.read(self.maxLength)

    def nextChar(self):
        if self.end:
            return ""
        if self.index >= len(self.bufferList[self.listIndex]):
            self.bufferList[self.listIndex] = self.cFile.read(10)
            self.listIndex = 1 - self.listIndex
            self.index = 0
            if len(self.bufferList[self.listIndex]) == 0:
                self.cFile.close()
                self.end = True
                return ""
        value = self.bufferList[self.listIndex][self.index]

        if value == "\n":
            self.line += 1
        self.index += 1
        return value

    def readAhead(self, next=0):
        if self.end:
            return ""
        nextIndex = self.index + next
        length = len(self.bufferList[self.listIndex])
        if nextIndex >= length:
            if nextIndex - length >= len(self.bufferList[1 - self.listIndex]):
                return ""
            value = self.bufferList[1 - self.listIndex][nextIndex - length]
            return value
        else:
            value = self.bufferList[self.listIndex][nextIndex]
            return value

boolTag=0
intTag=1
floatTag=2
normalStringTag=3
wideStringTag=4
charTag=5

leftBracketTag =6#{
rightBracketTag =7#}
commaTag =8#,

ifdefineTag =9
ifndefTag = 10
elseTag =11
endIfTag =12
defineTag = 13
undefTag =14

idTag = 15

'''只出现在结果中,PyMarcoParser.parse后出现在self.macroDic'''
tupleTag=16


class Token:
    tag=None
    value=None
    rawStr=None

    def __init__(self,tag,value=None,rawStr=None):
        self.tag=tag
        self.value=value
        self.rawStr=rawStr


def isEmpty(c):
    if len(c) != 1:
        return False
    return c == ' ' or c == '\n' or c == '\v' or c == '\r' or c == '\f' or c == '\t'


def isDigit(c):
    return c == "1" or c == "2" or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9" or c == "0"


letterList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z'
    , 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
              'X', 'Y', 'Z']

'''去除转义字符'''
def evalStr(st):
    index = 0
    length = len(st)
    result = ""
    while index < length:
        if st[index] == '\\':
            if st[index + 1] == '\\':
                result += '\\'
                index += 1
            elif st[index + 1] == '\'':
                result += '\''
                index += 1
            elif st[index + 1] == '\"':
                result += "\""
                index += 1
            elif st[index + 1] == 'a':
                result += chr(7)
                index += 1
            elif st[index + 1] == 'b':
                result += chr(8)
                index += 1
            elif st[index + 1] == "f":
                result += chr(12)
                index += 1
            elif st[index + 1] == "n":
                result = result + chr(10)
                index += 1
            elif st[index + 1] == "r":
                result = result + chr(13)
                index += 1
            elif st[index + 1] == "t":
                result = result + chr(9)
                index += 1
            elif st[index + 1] == "v":
                result = result + chr(11)
                index += 1
            elif st[index + 1] == "x":
                number = 0
                try:
                    number = st[index + 2] + st[index + 3]
                    number = int(number, 16)
                    index = index + 3
                except IndexError:
                    number = st[index + 2]
                    number = int(number, 16)
                    index = index + 2
                except ValueError:
                    number = st[index + 2]
                    number = int(number, 16)
                    index = index + 2
                # if number!=0:
                result = result + chr(number)
            # elif ord(st[index+1])==10:
            #   index=index+1
            elif isDigit(st[index + 1]):
                j = 3
                while index + j >= length:
                    j = j - 1

                number = ""
                c = ""
                while True:
                    i = 1
                    number = ""
                    while i <= j:
                        number += st[index + i]
                        i = i + 1
                    try:
                        number = int(number, 8)
                        c = chr(number)
                        break
                    except ValueError:
                        j = j - 1
                        pass
                # if number != 0:
                result = result + c
                index = index + j
            else:
                # raise RuntimeWarning("\\后不可识别的字符"+st[index+1])
                index += 1
                result = result + st[index]
        else:
            result += st[index]
        index += 1
    return result


'''是否是字母'''
def isLetter(c):
    return c in letterList


'''是否是换行'''
def isNewLine(c):
    return c == "\n" or c == "\r"

def tupleTokenToTuple(token):
    li = []
    for t in token.value:
        if t.tag == tupleTag:
            li.append(tupleTokenToTuple(t))
        else:
            if t.tag==normalStringTag:
                li.append(t.value)
            elif t.tag==wideStringTag:
                li.append(unicode(t.value,"utf-8"))
            else:
                li.append(t.value)
    return tuple(li)

def tupleFunction(token):
    result = ""
    for c in token.value:
        if c.tag == tupleTag:
            result = result + "," + tupleFunction(c)
        elif c.tag==boolTag:
                if c.value:
                    result=result+",true"
                else:
                    result=result+",false"
        elif c.tag==wideStringTag:
           result=result+",L\""+c.rawStr+"\""
        elif c.tag==normalStringTag:
            result=result+",\""+c.rawStr+"\""
        else:
            result = result + "," + str(c.value)

            # result = result + "," + tokenToStrFunction[c.tag](c)
    result = result.replace(",", "", 1)
    return "{" + result + "}"

class PyMacroParser:

    '''状态标志'''
    state=0
    '''传给下一个状态的字符串'''
    st=""
    '''token序列'''
    tokenQueue=[]
    '''结果'''
    macroDic={}
    '''是否需要再次解析'''
    needParse=True

    def __init__(self):
        # type: () -> object
        self.state = 0
        self.st = ""
        self.tokenQueue = []
        self.macroDic={}
        self.needParse=True
        pass

    def load(self, f):
        self.state = 0
        self.st = ""
        self.tokenQueue = []
        self.macroDic = {}
        self.needParse = True
        r=BufferReader(f)

        while not r.end:
            result=stateMachine[self.state](self,r)
            if result[0]:
                self.state=0
                self.st=""
                if result[1] is not None:
                     self.tokenQueue.append(result[1])
                else:
                    raise RuntimeError()
                pass
        pass

    def dump(self, f):
        self.parse()
        fi = open(f, "w+")
        for key, value in self.macroDic.items():
            fi.write("#define ")
            fi.write(key + " ")
            if value is None:
                pass
            elif value.tag==boolTag:
                if value.value:
                    fi.write("true")
                else:
                    fi.write("false")
            elif value.tag==wideStringTag:
                if value.rawStr is not None:
                    fi.write("L\"" + value.rawStr + "\"")
                else:
                    fi.write("L\""+value.value+"\"")
            elif value.tag==normalStringTag:
                if value.rawStr is not None:
                    fi.write("\"" + value.rawStr + "\"")
                else:
                    fi.write("\""+value.value+"\"")
            elif value.tag==tupleTag:
                fi.write(tupleFunction(value))
            else:
                fi.write(str(value.value))
            fi.write("\n")
        fi.close()
        pass

    def dumpDict(self):
        self.parse()
        result = {}
        for key, value in self.macroDic.items():
            if value is not None:
                if value.tag==normalStringTag:
                    st=value.value
                    result[key]=st
                elif value.tag==wideStringTag:
                    st = value.value
                    result[key]=unicode(st,"utf-8")
                elif value.tag==tupleTag:
                    result[key]=tupleTokenToTuple(value)
                else:
                    result[key] = value.value
            else:
                result[key] = None
        return result

    def preDefine(self, s):
        self.needParse = True
        self.macroDic.clear()
        li = s.split(";")
        for item in li:
            if item != "" and not isEmpty(item):
                self.macroDic[item] = None
        pass

    def parse(self):
        if not self.needParse:
            return
        parseStack = [True]
        index = 0
        while index < len(self.tokenQueue):
            if self.tokenQueue[index].tag == ifdefineTag:
                result = parseStack[len(parseStack) - 1] and self.tokenQueue[index + 1].value in self.macroDic
                parseStack.append(result)
                index = index + 2
            elif self.tokenQueue[index].tag == ifndefTag:
                result = parseStack[len(parseStack) - 1] and \
                         self.tokenQueue[index + 1].value not in self.macroDic
                parseStack.append(result)
                index = index + 2
            elif self.tokenQueue[index].tag == elseTag:
                result = parseStack.pop()
                parseStack.append(not result and parseStack[len(parseStack) - 1])
                index = index + 1
            elif self.tokenQueue[index].tag == endIfTag:
                parseStack.pop()
                index = index + 1

            elif self.tokenQueue[index].tag == undefTag:
                s = self.tokenQueue[index + 1].value
                if parseStack[len(parseStack) - 1]:
                    if s in self.macroDic:
                        self.macroDic.pop(s)
                index = index + 2

            elif self.tokenQueue[index].tag == defineTag:
                if self.tokenQueue[index + 1].value in self.macroDic and False:
                    raise RuntimeError(
                        "重复宏定义:" + self.tokenQueue[index + 1].value + "  " + str(self.tokenQueue[index + 2].value))
                else:
                    key = self.tokenQueue[index + 1].value
                    if index + 2 < len(self.tokenQueue) and self.tokenQueue[index + 2].value is not None:
                        value =self.tokenQueue[index + 2]
                        index=index+3
                        if value.tag== wideStringTag or value.tag==normalStringTag:
                            value = Token(value.tag, evalStr(value.value),
                                          value.value)
                            while index<len(self.tokenQueue) and (self.tokenQueue[index].tag == wideStringTag or self.tokenQueue[index].tag==normalStringTag):
                                value.value=value.value+evalStr(self.tokenQueue[index].value)
                                value.rawStr=value.rawStr+"\"\""+self.tokenQueue[index].value
                                if self.tokenQueue[index].tag == wideStringTag:
                                    value.tag=wideStringTag
                                index=index+1
                        if parseStack[len(parseStack) - 1]:
                            self.macroDic[key] = value

                    elif index+2<len(self.tokenQueue) and self.tokenQueue[index+2].tag ==leftBracketTag:
                        index=index+2
                        tupleStack=[]
                        while index<len(self.tokenQueue):
                            if self.tokenQueue[index].tag==leftBracketTag:
                                tupleStack.append(Token(tupleTag,[]))
                            elif self.tokenQueue[index].tag==intTag or \
                                self.tokenQueue[index].tag==floatTag or self.tokenQueue[index].tag==boolTag \
                                or self.tokenQueue[index].tag==charTag:
                                tupleStack[len(tupleStack)-1].value.append(self.tokenQueue[index])
                            elif self.tokenQueue[index].tag== wideStringTag or self.tokenQueue[index].tag==normalStringTag:
                                tupleStack[len(tupleStack) - 1].value.append(Token(self.tokenQueue[index].tag,evalStr(self.tokenQueue[index].value),self.tokenQueue[index].value))
                                while index+1<len(self.tokenQueue) and (self.tokenQueue[index+1].tag == wideStringTag or self.tokenQueue[index+1].tag==normalStringTag):
                                    tupleStack[len(tupleStack) - 1].value[len(tupleStack[len(tupleStack) - 1].value)-1].value+=evalStr(self.tokenQueue[index+1].value)
                                    tupleStack[len(tupleStack) - 1].value[
                                        len(tupleStack[len(tupleStack) - 1].value) - 1].rawStr +=("\"\""+self.tokenQueue[index + 1].value)

                                    if self.tokenQueue[index+1].tag == wideStringTag:
                                        tupleStack[len(tupleStack) - 1].value[len(tupleStack[len(tupleStack) - 1].value) - 1].tag=wideStringTag
                                    index=index+1
                            elif self.tokenQueue[index].tag==commaTag:
                                pass
                            elif self.tokenQueue[index].tag==rightBracketTag:
                                tu=tupleStack.pop()
                                length=len(tupleStack)
                                if length==0:
                                    index=index+1#消耗掉}
                                    if parseStack[len(parseStack) - 1]:
                                        self.macroDic[key] =tu
                                    break
                                else:
                                    tupleStack[length-1].value.append(tu)
                            else:
                                raise RuntimeError()
                            index=index+1
                        pass
                    else:

                        if parseStack[len(parseStack) - 1]:
                            self.macroDic[key] = None
                        index=index+2
            elif self.tokenQueue[index].tag == normalStringTag or self.tokenQueue[index].tag == wideStringTag:
                index=index+1
               #raise RuntimeError()
            elif self.tokenQueue[index].tag==intTag:
                raise RuntimeError()
            elif self.tokenQueue[index].tag==floatTag:
                raise RuntimeError()
            elif self.tokenQueue[index].tag==boolTag:
                raise RuntimeError
            elif self.tokenQueue[index].tag==charTag:
                raise RuntimeError
            elif self.tokenQueue[index].tag==idTag:
                raise RuntimeError
            else:
                raise RuntimeError('匹配出错')
        self.needParse = False
        pass


#初始状态
def state0(PyMacroParser,BufferReader):
    c=BufferReader.readAhead()
    if c=="/" and BufferReader.readAhead(1)=="/":
        PyMacroParser.state=1
        return False,None
    elif c=="/" and BufferReader.readAhead(1)=="*":
        PyMacroParser.state=2
        return False,None
    elif c=="#":
        PyMacroParser.state=3
        return False,None
    elif isEmpty(c):
        passEmpty(BufferReader)
        return False,None

        '''宽字符和字符串在判断时带有内在顺序'''
    elif (c=="L" or c=="l") and BufferReader.readAhead(1)=="\"":
        PyMacroParser.state=12
        return False,None
        pass
    elif c=="\"":
        PyMacroParser.state=11
        return False,None
        pass
    elif (c=="L" or c=="l") and BufferReader.readAhead(1)=="\'":
        raise RuntimeError()
    elif c=="\'":
        PyMacroParser.state=13
        return False,None
        pass
    elif isLetter(c) or c=="_":
        PyMacroParser.state=4
        return False,None
        pass

        '''这三种情况判断时带有内在顺序'''
    elif c=="0" and (BufferReader.readAhead(1)=="X" or BufferReader.readAhead(1)=="x"):
        PyMacroParser.state=5
        return False,None
    elif c=="0":
        PyMacroParser.state=7
        return False,None
    elif isDigit(c):
        PyMacroParser.state=6
        return False,None
    elif c==".":
        PyMacroParser.state=8
        return False,None
    elif c=="":
        BufferReader.nextChar()
        return False,None
    elif c=="+" or c=="-":
        PyMacroParser.state=9
        return False,None
    elif c=="{":
        BufferReader.nextChar()
        return True,Token(leftBracketTag)
        pass
    elif c=="}":
        BufferReader.nextChar()
        return True,Token(rightBracketTag)
        pass
    elif c==",":
        BufferReader.nextChar()
        return True,Token(commaTag)
        #
        pass
    elif c==";":
        BufferReader.nextChar()
        raise RuntimeError()
    else:
        BufferReader.nextChar()
        raise RuntimeError()

def passEmpty(BufferReader):
    c=BufferReader.readAhead()
    while isEmpty(c):
        BufferReader.nextChar()
        c=BufferReader.readAhead()

'''将后缀消耗掉'''
def integerPostfix(BufferReader):
    c=BufferReader.readAhead()
    if c == "l" or c == "L":
        BufferReader.nextChar()
        c = BufferReader.readAhead()
        if c == "l" or c == "L":
            BufferReader.nextChar()
            c = BufferReader.readAhead()
            if c == "u" or c == "U":
                BufferReader.nextChar()  # llu
                c = BufferReader.readAhead()
        elif c == "u" or c == "U":
            BufferReader.nextChar()
            c = BufferReader.readAhead()
            if c == "l" or c == "L":
                BufferReader.nextChar()
                c = BufferReader.readAhead()  # lul
    elif c == "u" or c == "U":
        BufferReader.nextChar()
        c = BufferReader.readAhead()
        if c == "l" or c == "L":
            BufferReader.nextChar()
            c = BufferReader.readAhead()
            if c == "l" or c == "L":
                BufferReader.nextChar()
                c = BufferReader.readAhead()
        elif (c == 'i' or c == 'I') and BufferReader.readAhead(1) == '6' and BufferReader.readAhead(2) == '4':
            BufferReader.nextChar()
            BufferReader.nextChar()
            BufferReader.nextChar()
    elif (c == 'i' or c == 'I') and BufferReader.readAhead(1) == '6' and BufferReader.readAhead(2) == '4':
        BufferReader.nextChar()
        BufferReader.nextChar()
        BufferReader.nextChar()

'''//注释只有0跳转过来'''
def state1(PyMacroParser,BufferReader):

    if not(BufferReader.readAhead(0)=="/" and BufferReader.readAhead(1)=="/"):
        raise RuntimeError()
    BufferReader.nextChar()
    BufferReader.nextChar()
    last =""
    c = BufferReader.nextChar()
    while (not isNewLine(c) or (isNewLine(c) and last == "\\")) and c != "":
        last = c
        c = BufferReader.nextChar()
    PyMacroParser.state = 0
    return False,None

'''/**/注释只有0跳转过来，但是3，9直接使用了这个方法'''
def state2(PyMacroParser,BufferReader):
    if BufferReader.readAhead(0)!="/" or BufferReader.readAhead(1)!="*":
        raise RuntimeError()
    BufferReader.nextChar()
    BufferReader.nextChar()
    while True:
        if BufferReader.readAhead(0)=="*" and BufferReader.readAhead(1)=="/":
            break
        BufferReader.nextChar()
    BufferReader.nextChar()
    BufferReader.nextChar()
    PyMacroParser.state=0
    return False,None

'''预处理指令#只有0跳转过来'''
def state3(PyMacroParser,BufferReader):
    st =BufferReader.nextChar()
    if st!="#":
        raise RuntimeError()
    c=BufferReader.readAhead()
    if c=="#":
        #出现##
        raise RuntimeError()
    # #  /*123*/ /*456*/  define
    passEmpty(BufferReader)
    while BufferReader.readAhead(0) == "/" and BufferReader.readAhead(1)== "*":
        state2(PyMacroParser,BufferReader)
        passEmpty(BufferReader)
    c=BufferReader.readAhead()

    while isLetter(c) or isDigit(c) or c=="_":
        st+=c
        BufferReader.nextChar()
        c=BufferReader.readAhead()
    if st=="#define":
        return True,Token(defineTag)
    elif st=="#undef":
        return True,Token(undefTag)
    elif st=="#ifdef":
        return True,Token(ifdefineTag)
    elif st=="#ifndef":
        return True,Token(ifndefTag)
    elif st=="#else":
        return True,Token(elseTag)
    elif st=="#endif":
        return True,Token(endIfTag)
    else:
        raise RuntimeError("在第"+str(BufferReader.line)+"行无法识别的操作")

'''变量名和true，false只有0跳转过来'''
def state4(PyMacroParser,BufferReader):
    c = BufferReader.readAhead()
    if not isLetter(c) and c!="_":
        raise RuntimeError()
    st=""
    while isLetter(c) or isDigit(c) or c=="_":
        st+=c
        BufferReader.nextChar()
        c=BufferReader.readAhead()
    if st == "true":
        return True, Token(boolTag, True)
    elif st == "false":
        return True, Token(boolTag, False)
    else:
        return True,Token(idTag,st)
    pass

'''0x开头的十六进制,由0和9跳转过来'''
def state5(PyMacroParser,BufferReader):
    if BufferReader.readAhead()!="0" and (BufferReader.readAhead(1)!="X" or BufferReader.readAhead(2)!="x"):
        raise RuntimeError()
    BufferReader.nextChar()
    BufferReader.nextChar()
    #由9跳转过来时含有"+"或"-"
    if PyMacroParser.st!="+" and PyMacroParser.st!="-" and PyMacroParser.st!="":
        raise  RuntimeError()
    st=PyMacroParser.st+"0X"
    c=BufferReader.readAhead()
    while isDigit(c) or  (c == 'a' or c == 'A' or c == 'b' or c == 'B' or c == 'c'
                                        or c == 'C' or c == 'd' or c == 'D' or c == 'e' or c == 'E' or c == 'F' or c == 'f'):
        st += c
        BufferReader.nextChar()
        c =BufferReader.readAhead()
    integerPostfix(BufferReader)
    return True,Token(intTag,int(st,16))

'''数字开头不包括0 整型由0和9跳转过来
碰到.点跳转到8
碰到e or E跳到10'''
def state6(PyMacroParser,BufferReader):

    if not isDigit(BufferReader.readAhead()):
        raise RuntimeError()
    #如果由9跳转过来那么PyMacroParser.st会含有一个+或-
    #如果由0跳转过滤那么PyMacroParser.st是空字符串
    if PyMacroParser.st!="+" and PyMacroParser.st!="-" and PyMacroParser.st!="":
        raise RuntimeError()
    st=PyMacroParser.st
    c=BufferReader.readAhead()
    while isDigit(c):
        st += c
        BufferReader.nextChar()  # 消耗一个字符
        c = BufferReader.readAhead()
    if c == "U" or c == 'u':
        if st[0] == '-':
            raise RuntimeError("-操作符不能用在无符号整型上")
        BufferReader.nextChar()
        c = BufferReader.readAhead()
        #u结尾如果后面都不满足的话
        if (c == 'i' or c == 'I') and BufferReader.readAhead(1) == '6' and BufferReader.readAhead(2) == '4':
            BufferReader.nextChar()
            BufferReader.nextChar()
            BufferReader.nextChar()
            #ui64结尾
        elif c == 'L' or c == 'l':
            BufferReader.nextChar()
            c = BufferReader.readAhead()
            #ul结尾
            if c == 'L' or c == 'l':
                BufferReader.nextChar()
                #ull结尾
    elif c == 'L' or c == 'l':

        BufferReader.nextChar()
        c = BufferReader.readAhead()
        #l结尾
        if c == 'U' or c == 'u':
            BufferReader.nextChar()
            c = BufferReader.readAhead()
            if st[0] == '-':
                raise RuntimeError("-操作符不能用在无符号整型上")
            #lu结尾
            if c == 'L' or c == 'l':
                BufferReader.nextChar()
                c = BufferReader.readAhead()
                #lul结尾
        elif c == 'L' or c == 'l':
            BufferReader.nextChar()
            c = BufferReader.readAhead()
            #ll结尾
            if c == 'U' or c == 'u':
                #llu结尾
                BufferReader.nextChar()
    elif (c == 'i' or c == 'I') and BufferReader.readAhead(1) == '6' and BufferReader.readAhead(2) == '4':
        BufferReader.nextChar()
        BufferReader.nextChar()
        BufferReader.nextChar()
        #i64结尾

    elif c == "F" or c == 'f':
        #f结尾
       raise RuntimeError()
    elif c==".":
        PyMacroParser.st=st
        PyMacroParser.state=8
        return False,None
    elif c=="e" or c=="E":
        PyMacroParser.st = st
        PyMacroParser.state = 10
        return False, None

    else:
        pass
    return True,Token(intTag,int(st))
    pass

'''八进制开头一定有0,由0和9跳转过来
碰到.点跳转到8
碰到e or E跳到10'''
def state7(PyMacroParser,BufferReader):
    if BufferReader.readAhead()!="0":
        raise  RuntimeError()
    if PyMacroParser.st!="+" and PyMacroParser.st!="-" and PyMacroParser.st!="":
        raise  RuntimeError()
    c=BufferReader.nextChar()#把0加上
    st=PyMacroParser.st+c
    c=BufferReader.readAhead()
    while c =="0" or c=="1" or c=="2" or c=="3" or c=="4" or c=="5" or c=="6" or c=="7":
        st=st+c
        BufferReader.nextChar()
        c=BufferReader.readAhead()
    if c==".":
        PyMacroParser.st=st
        PyMacroParser.state=8
        return False,None
    elif c=="e" or c=="E":
        PyMacroParser.st = st
        PyMacroParser.state = 10
        return False, None
    else:
        integerPostfix(BufferReader)
        return True,Token(intTag,int(st,8))
    pass

'''.开头，带点的小数 .交给这个函数处理
由6和7跳转过来
碰到e跳装到10'''
def state8(PyMacroParser,BufferReader):
    if BufferReader.readAhead()!=".":
        raise RuntimeError()
    c = BufferReader.nextChar()
    st=PyMacroParser.st+c
    c = BufferReader.readAhead()
    while isDigit(c) and c != "":
        st += c
        BufferReader.nextChar()
        c=BufferReader.readAhead()

    if c=="e" or c=="E":
        PyMacroParser.st=st
        PyMacroParser.state=10
        return False,None
    elif c=="f" or c=="F":
        '''后缀为f的float'''
        BufferReader.nextChar()
    elif c=="l" or c=="L":
        '''后缀为l的float'''
        BufferReader.nextChar()
    try:
        f=float(st)
        return True,Token(floatTag,f)
    except BaseException:
        raise RuntimeError("在"+str(BufferReader.line)+"行不合法的浮点数 小数点两边的数字不能同时省略")
    pass


'''+-号开头由0跳装过来
碰到0x or 0X跳到5
碰到0开头跳到7
碰到其他数字跳到6
碰到.跳到8'''
def state9(PyMacroParser,BufferReader):
    if BufferReader.readAhead()!="+" and BufferReader.readAhead()!="-":
        raise RuntimeError()
    PyMacroParser.st=BufferReader.nextChar()

    #考虑+  /*abc  */   /*123123aff*/  123
    passEmpty(BufferReader)
    while BufferReader.readAhead(0) == "/" and BufferReader.readAhead(1) == "*":
        state2(PyMacroParser, BufferReader)
        passEmpty(BufferReader)
    c = BufferReader.readAhead()
    if c=="0" and (BufferReader.readAhead(1)=="X" or BufferReader.readAhead(1)=="x"):
        PyMacroParser.state=5
        return False,None
    elif c=="0":
        PyMacroParser.state=7
        return False,None
    elif isDigit(c):
        PyMacroParser.state=6
        return False,None
    elif c==".":
        PyMacroParser.state=8
        return False,None
    elif c=="+" or c=="-":
        raise  RuntimeError("++/--")
    else:
        raise  RuntimeError("在"+str(BufferReader.line)+"行+/-号后面出现违法字符")
    pass

'''带E or e的指数形式 e or E交给这个函数处理
由6，7,8跳转过来'''
def state10(PyMacroParser,BufferReader):
    c=BufferReader.readAhead()
    if c!="e" and c!="E":
        raise RuntimeError()
    st=PyMacroParser.st
    st+=c
    BufferReader.nextChar()
    c=BufferReader.readAhead()
    if c=="+" or c=="-":
        st+=c
        BufferReader.nextChar()
        c=BufferReader.readAhead()
    while isDigit(c):
        st=st+c
        BufferReader.nextChar()
        c=BufferReader.readAhead()
    if c=="f" or c=="F":
        BufferReader.nextChar()
    elif c=="l" or c=="L":
        BufferReader.nextChar()
    f=float(st)
    return True,Token(floatTag,f)
    pass


'''左双引号在调用方使用掉了'''
def getString(BufferReader):
    st = ""
    count = 0
    c=BufferReader.readAhead()
    while c != '':
        if c == "\"" and count % 2 == 0:
            break
        # "\\\""  "\\" 连续的\碰到"如果是偶数那么"是字符串结尾
        if c == '\\':
            count += 1
        else:
            count = 0
        st += c
        BufferReader.nextChar()
        c = BufferReader.readAhead()
    return st
'''普通字符串由0跳过来'''
def state11(PyMacroParser,BufferReader):
    c=BufferReader.nextChar()
    if c!="\"":
        raise RuntimeError()
    st=getString(BufferReader)
    c = BufferReader.readAhead()
    if c=="\"":
        BufferReader.nextChar()
        return True,Token(normalStringTag,st)
    else:
        raise RuntimeError("在第"+str(BufferReader.line)+"行字符串没有右引号")
    pass
'''宽字符串由0跳转过来'''
def state12(PyMacroParser,BufferReader):
    c = BufferReader.nextChar()
    if c != "L" and c!="l"and BufferReader.readAhead()!="\"":
        raise RuntimeError()
    BufferReader.nextChar()
    st = getString(BufferReader)
    c = BufferReader.readAhead()
    if c == "\"":
        BufferReader.nextChar()
        return True, Token(wideStringTag, st)
    else:
        raise RuntimeError("在第" + str(BufferReader.line) + "行字符串没有右引号")
    pass
    pass
'''字符由0跳转过来'''
def state13(PyMacroParser,BufferReader):
    c=BufferReader.nextChar()
    if c!="\'":
        raise RuntimeError()
    st = ""
    count = 0
    c=BufferReader.readAhead()
    while c != '':
        if c == "\'" and count % 2 == 0:
            break
        # "\\\""  "\\" 连续的\碰到"如果是偶数那么"是字符串结尾
        if c == '\\':
            count += 1
        else:
            count = 0
        st += c
        BufferReader.nextChar()
        c = BufferReader.readAhead()
    if c == '\'':
        BufferReader.nextChar()
        s = evalStr(st)
        length = len(s)
        if length > 0:
            return True, Token(charTag, ord(s[length - 1]))
        else:
            return True, Token(charTag, '')
            pass
    else:
        raise RuntimeError("在第" + str(BufferReader.line) + "行字符没有以\'结束")
    pass

stateMachine={0:state0,1:state1,2:state2,3:state3,4:state4,5:state5,
              6:state6,7:state7,8:state8,9:state9,10:state10,11:state11,
              12:state12,13:state13}







