# -*- coding: UTF-8 -*-
from PyMacroParser import PyMacroParser
import PyMacroParser as pm


letterlist = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W',
              'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
              's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
def test1():
    py = PyMacroParser()
    py.load("test1")
    print py.dumpDict()
    py.dump("1.txt")
def test2():
    py = PyMacroParser()
    py.load("test2")
    print py.dumpDict()
    py.dump("2.txt")
def test3():
    py = PyMacroParser()
    py.load("test3")
    i=0
    while i<len(py.tokenQueue):
        assert py.tokenQueue[i].tag==pm.defineTag
        assert py.tokenQueue[i+1].tag==pm.idTag
        if py.tokenQueue[i+1].value!=letterlist[int(i/3)]:
            print py.tokenQueue[i+1].value,letterlist[int(i/3)]
            raise RuntimeError()
        i=i+3
    assert py.tokenQueue[2].tag==pm.intTag
    assert py.tokenQueue[2].value==10
    assert py.tokenQueue[5].tag==pm.floatTag
    assert py.tokenQueue[5].value==123.456
    assert py.tokenQueue[8].tag==pm.intTag
    assert py.tokenQueue[8].value==90123
    assert py.tokenQueue[11].tag==pm.floatTag
    assert py.tokenQueue[11].value==0.45899
    print py.dumpDict()
    py.dump("3.txt")
def test4():
    py=PyMacroParser()
    py.load("test4")
    i = 0
    while i < len(py.tokenQueue):
        assert py.tokenQueue[i].tag == pm.defineTag
        assert py.tokenQueue[i + 1].tag == pm.idTag
        if py.tokenQueue[i + 1].value != letterlist[26+int(i / 3)]:
            print py.tokenQueue[i + 1].value, letterlist[26+int(i / 3)]
            raise RuntimeError()
        i = i + 3
    print py.dumpDict()
    py.dump("4.txt")
def test5():
    py=PyMacroParser()
    py.load("test5")
    i=0
    while i<len(py.tokenQueue):
        if py.tokenQueue[i].tag!=pm.defineTag:
            print i
            raise RuntimeError()
        if py.tokenQueue[i+1].tag!=pm.idTag:
            print i
            raise RuntimeError()
        if py.tokenQueue[i+1].value!="d"+str(((i/3)+1)):
            print i
            raise RuntimeError()
        i=i+3
    print py.dumpDict()
    py.dump("5.txt")

def test6():
    py = PyMacroParser()
    py.load("test6")
    print py.dumpDict()
    py.dump("6.txt")

def test7():
    py = PyMacroParser()
    py.load("test7")
    print py.dumpDict()
    py.dump("7.txt")

test1()
test2()
test3()
test4()
test5()
test6()
test7()


