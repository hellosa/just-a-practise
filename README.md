# 酒店智能客服系统

## 基于提供的数据，实现一个智能的酒店客服系统。核心功能如下：
* 价格区间检索：用户可以指定一个价格区间，如 300-500 元，系统返回此价格范围内的酒店列表。
* 名称检索：用户可以直接输入酒店名称或部分名称进行查询，系统会返回与该名称匹配或相近的酒店。
* 评分检索：用户可以选择查找高于或低于某一评分的酒店。
* 设施检索：用户可以根据需要的设施（如游泳池、健身房、WIFI）来筛选酒店。
* 多轮对话：系统能够理解用户的多轮对话上下文，例如：提出“我要一个有游泳池的酒店”后，再提要求“价格在 500 元以下的”。
* 安全防护：系统设计时需注意输入检查与处理，防止恶意代码或输入导致系统崩溃或数据泄露。

---
### create the env
	python3 -m venv venv
	
### enter the env
	source venv/bin/activate
	
### install the packages
	pip install -r requirements.txt
	
### create a sql db: json -> db
	python import_db.py
	
### create a .env
	cp .env.example .env # and fill the blank
	
### launch the gradio
	python webui.py
	or
	gradio webui.py # auto reload