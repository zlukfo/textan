Тезаурус EUROVOC
================
Скачать исходные RDF-файлы можно `здесь <https://op.europa.eu/bg/web/eu-vocabularies/th-dataset/-/resource/dataset/eurovoc>`_
Из данного репозитория можно скачать распарсенные файлы в форматах sqlite3 и json
Подробнее можно прочитать в `статье <http://lukfo.online/articles/eurovoc/>`_ 

Пример использования
--------------------
**1. По поисковому запросу найти дескриптор (слово или сочетание) и вывести в виде графа все его связи в тезаурусе**

.. code-block:: python

  from graphviz import Graph
  import sqlite3

  SEARCH='региони на Дания'
  connection = sqlite3.connect('eurovoc.sqlite3')
  cursor=connection.cursor()
  sql='''
  select descriptors.id, prefLabel, rel.rel_name, lang from descriptors,     
    (select rel_val as id, rel_name from relations
      inner join (
        select id, prefLabel from descriptors where prefLabel like '{}%' and lang='bg'
      ) using (id)
    ) as rel
  where rel.id=descriptors.id and lang='bg'
  '''.format(SEARCH)

  node_attr={'fontcolor':'red'}
  graph_attr={'size':"6,15",'overlap':'false','rankdir':'LR'}
  edge_attr={'len':'2'}
  dot = Graph(node_attr=node_attr, graph_attr=graph_attr, edge_attr=edge_attr, engine='dot', format='svg')
  dot.node(SEARCH)

  result=cursor.execute(sql)
  result=[i for i in result]
  for s in set([i[2] for i in result]):
      with dot.subgraph(name=s, node_attr={'shape': 'box'}) as c:
          c.edges([(SEARCH, res[1]) for res in result if res[2]==s])
  dot
