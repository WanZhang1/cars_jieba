#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by zhangw 2017/11/8
from flask import Flask, abort, request, jsonify
import jieba
import jieba.posseg as pseg
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

app = Flask(__name__)

# 自定义词典
jieba.load_userdict("dict/accidentDepart.dat")
jieba.load_userdict("dict/accidentName.dat")
jieba.load_userdict("dict/originAccidentLocale.dat")
# 铁路专业词典
jieba.load_userdict("dict/general.dat")
jieba.load_userdict("dict/railDictionary.dat")
# 铁路客运站点
jieba.load_userdict("dict/stationDictionary.dat")
# 货运线路
jieba.load_userdict("dict/freightLine.dat")
# 货运站点
jieba.load_userdict("dict/freightStation.dat")

# 事故专业词典
jieba.load_userdict("dict/locale_ok.dat")
jieba.load_userdict("dict/name_ok.dat")
jieba.load_userdict("dict/reason_ok.dat")
jieba.load_userdict("dict/depart_ok.dat")



# 添加词语到词典，可以添加多个，用 | 分隔开
@app.route('/dict_add', methods=['POST'])
def dict_add():
	if not request.json or 'words' not in request.json or 'file' not in request.json:
		abort(400)
	words = request.json['words']
	file = request.json['file']
	
	f = open("dict/"+file, 'a')
	w = words.split("|")
	
	for i in range(0,len(w)):
		f.write("\n"+w[i])
	
	f.close()
	
	return "Success"


# 从词典删除词语,删除单个词语
@app.route('/dict_del', methods=['POST'])
def dict_del():
	if not request.json or 'word' not in request.json or 'file' not in request.json:
		abort(400)
	word = request.json['word']
	file = request.json['file']
	
	
	f= open("dict/"+file, "r")
	lines = f.readlines()
	f_w=open("dict/"+file, "w")
	for line in lines:
		if word in line:
			print(word + "," + line)
			continue
		f_w.write(line)
	
	f.close()
	f_w.close()
	
	return "Success"

#单个文本
@app.route('/jieba_parse', methods=['POST'])
def user_dict():
	if not request.json or 'text' not in request.json:
		abort(400)
	text = request.json['text']
	
	
	seg_list = jieba.cut(text, cut_all=False)
	seg = " ".join(seg_list)
	print(seg)
	
	return  seg


# 单个段落，词性标注，\t键分隔    word   词性
@app.route('/word_flag', methods=['POST'])
def word_flag():
	if not request.json or 'text' not in request.json:
		abort(400)
	text = request.json['text']
	words = pseg.cut(text)
	seg=''
	for word, flag in words:
		seg=seg+'\n'+word+'\t'+flag
	return  seg


# 单个文件：传入文件路径及文件名（单个文件），\t分隔    word   词性
@app.route('/batch_flag', methods=['POST'])
def batch_word_flag():
	if not request.json or 'path' not in request.json:
		abort(400)
	path = request.json['path']
	if os.path.isfile(path):
		print("文件：" + path)
		f = open(path, 'rb')
		text = f.read()
		words = pseg.cut(text)
	seg=''
	for word, flag in words:
		seg=seg+'\n'+word+'\t'+flag
	#print("seg:"+seg)
	return  seg


# 批量处理：传入文件路径（多个文件），写入输出路径 \t键分隔    word   词性
@app.route('/file_flag', methods=['POST'])
def file_word_flag():
	if not request.json or 'path' not in request.json or 'output' not in request.json:
		abort(400)
	rootdir = request.json['path']
	output = request.json['output']
	
	list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
	
	for i in range(0, len(list)):
		path = os.path.join(rootdir, list[i])
		if os.path.isfile(path):
			print("文件：" + path)
			file_object = open(output + list[i], 'w', encoding='utf-8')
			
			f = open(path, 'rb')
			text = f.read()
			words = pseg.cut(text)
			seg=''
			for word, flag in words:
				seg = seg + '\n' + word + '\t' + flag
			
			file_object.write(seg)
			
			f.close()
			file_object.close()
	
	return jsonify({'result': 'Success'})
		


#批量处理，传入文件路径，指定文件输出路径
@app.route('/batch_parse', methods=['POST'])
def batch_parse():
	if not request.json or 'path' not in request.json or 'output' not in request.json:
		abort(400)
	rootdir = request.json['path']
	output = request.json['output']
	
	list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
	
	for i in range(0, len(list)):
		path = os.path.join(rootdir, list[i])
		if os.path.isfile(path):
			print("文件：" + path)
			file_object = open(output+list[i], 'w',encoding='utf-8')
			
			f = open(path,'rb')
			text = f.read()
			seg_list = jieba.cut(text, cut_all=False)
			seg = " ".join(seg_list)
			print(seg)
			
			file_object.write(seg)
			
			f.close()
			file_object.close()
			
	return jsonify({'result': 'Success'})

if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", debug=True)

