import os.path
from whoosh.index import create_in
from whoosh.fields import *

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
dir_path = os.path.dirname(os.path.realpath(__file__))
ix = create_in(dir_path + "/whoosh_index", schema)
writer = ix.writer()

writer.add_document(
    title=u"First document",
    path=u"/a",
    content=u"This is the first document we've added!")
writer.add_document(
    title=u"Second document",
    path=u"/b",
    content=u"The second one is even more interesting!")
writer.commit()

from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("first")
    results = searcher.search(query)
    print(results[0])
