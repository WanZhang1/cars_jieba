# encoding=utf-8

import sys
sys.path.append("../")

import jieba
import jieba.posseg
import jieba.analyse



#读取文档内容
f = open("../../../file/9.17护网内有行人情况.docx", 'rb')

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
