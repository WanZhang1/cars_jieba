#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by zhangw 2017/11/8
from flask import Flask, abort, request, jsonify
import jieba

app = Flask(__name__)

@app.route('/jieba_parse/', methods=['POST'])
def jieba_parse():
    if not request.json or 'text' not in request.json :
        abort(400)
    text=request.json['text']
    seg_list = jieba.cut(text, cut_all=False)
    seg = " ".join(seg_list)
    print( seg)
    
    return jsonify({'result': seg})


@app.route('/user_dict/', methods=['POST'])
def user_dict():
	if not request.json or 'text' not in request.json:
		abort(400)
	text = request.json['text']
	
	# 自定义词典
	jieba.load_userdict("../../../file/accidentDepart.dat")
	jieba.load_userdict("../../../file/accidentGrade.dat")
	jieba.load_userdict("../../../file/accidentLocale.dat")
	jieba.load_userdict("../../../file/accidentName.dat")
	jieba.load_userdict("../../../file/originAccidentLocale.dat")
	seg_list = jieba.cut(text, cut_all=False)
	seg = " ".join(seg_list)
	print(seg)
	
	return jsonify({'result': seg})

if __name__ == "__main__":
    # 将host设置为0.0.0.0，则外网用户也可以访问到这个服务
    app.run(host="0.0.0.0", debug=True)

