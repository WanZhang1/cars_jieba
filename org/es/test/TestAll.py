# encoding=utf-8

import sys
sys.path.append("../")

import jieba
import jieba.posseg
import jieba.analyse



#获取文档内容
#读取文档内容
f = open("../../../file/9.21机车玻璃破损信息.docx", 'rb')

fullText = f.read()

f.close()

#自定义词典
jieba.load_userdict("../../../file/accidentDepart.dat")
jieba.load_userdict("../../../file/accidentGrade.dat")
jieba.load_userdict("../../../file/accidentLocale.dat")
jieba.load_userdict("../../../file/accidentName.dat")
jieba.load_userdict("../../../file/originAccidentLocale.dat")

print('='*40)
print('1. 分词')
print('-'*40)


seg_list = jieba.cut(fullText, cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 默认模式



print('='*40)
print('2. 词性标注')
print('-'*40)

words = jieba.posseg.cut(fullText)
for word, flag in words:
    print('%s %s' % (word, flag))


print('='*40)
print('3. 添加自定义词典/调整词典')
print('-'*40)

print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
#如果/放到/post/中将/出错/。
print(jieba.suggest_freq(('中', '将'), True))
#494
print('/'.join(jieba.cut('如果放到post中将出错。', HMM=False)))
#如果/放到/post/中/将/出错/。
print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
#「/台/中/」/正确/应该/不会/被/切开
print(jieba.suggest_freq('台中', True))
#69
print('/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
#「/台中/」/正确/应该/不会/被/切开


print('='*40)
print('4. 关键词提取')
print('-'*40)
print(' TF-IDF')
print('-'*40)


for x, w in jieba.analyse.extract_tags(fullText, withWeight=True):
    print('%s %s' % (x, w))

print('-'*40)
print(' TextRank')
print('-'*40)

for x, w in jieba.analyse.textrank(fullText, withWeight=True):
    print('%s %s' % (x, w))


print('='*40)
print('5. Tokenize: 返回词语在原文的起止位置')
print('-'*40)
print(' 默认模式')

print('-'*40)
result = jieba.tokenize(fullText)
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))

print('-'*40)
print(' 搜索模式')
print('-'*40)

result = jieba.tokenize(fullText, mode='search')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))