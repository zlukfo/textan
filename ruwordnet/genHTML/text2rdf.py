# -*- coding: utf-8 -*-
# Генератор html-страниц для дескрипторов тезаруруса
# парсит заданный файл и для каждого дескриптора (уровень 0)
# генерирует html-страницу в синтаксисе RDFa

# url к лескрипторам задается в шаблоне

from jinja2 import Template
import codecs
#import json

FILENAME="verb.txt"

descr={'descriptor':None, 'synsets':[]}
# в rels определены не все отношения, указанные в тезаурусе
# не описанные отношения игнорируются
rels={u'гипоним':'broader', u'гипероним': 'narrower', 
      u'мероним': 'inScheme', u'холоним': 'topConceptOf'	
}

def count0(line): 
	descr['descriptor']=line
def count1(line): 
	descr['synsets'].append({'description':line.split(', '), 'relations':{}})
def count2(line):
	global buff
	buff=rels.get(line)
	if buff:
		descr['synsets'][-1]['relations'].setdefault(buff,[])
def count3(line):
	if buff:
		descr['synsets'][-1]['relations'][buff].append(line)
getdata=(count0, count1, count2, count3)

data=[]
# ОТЛАДОЧНЫЙ счетчик - сколько дескрипторов сначала файла еужно распарсить
counter=4
with codecs.open(FILENAME, 'r', 'utf-8') as fd:
	for line in fd:
		if not counter:
			break
		if not '\t' in line and descr['descriptor']:
			data.append(descr.copy())
			descr['descriptor']=None
			descr['synsets']=[]
			counter-=1
		getdata[line.count('\t')](line[:-1].replace('\t',''))

#print json.dumps(data[1], indent=2, ensure_ascii=False)

# --- генератор шаблонов
html = open('templ.jinja').read()
template = Template(html.decode('utf-8'))
for d in data:
	# !!!??? транслитерация имен файлов?
	with codecs.open('test.html','w', 'utf-8') as fd:
		fd.write(template.render(d))



