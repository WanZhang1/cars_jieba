#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by zhangw 2017/11/8
from flask import Flask, abort, request, jsonify
import jieba
import jieba.posseg as pseg
import os

app = Flask(__name__)

# 自定义词典
jieba.load_userdict("../../../file/accidentDepart.dat")
jieba.load_userdict("../../../file/accidentGrade.dat")
jieba.load_userdict("../../../file/accidentLocale.dat")
jieba.load_userdict("../../../file/accidentName.dat")
jieba.load_userdict("../../../file/originAccidentLocale.dat")
# 铁路专业词典
jieba.load_userdict("../../../file/general.dat")
jieba.load_userdict("../../../file/railDictionary.dat")
# 铁路客运站点
jieba.load_userdict("../../../file/stationDictionary.dat")
# 货运线路
jieba.load_userdict("../../../file/freightLine.dat")
# 货运站点
jieba.load_userdict("../../../file/freightStation.dat")

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

