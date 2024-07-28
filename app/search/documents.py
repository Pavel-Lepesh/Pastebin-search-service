from elasticsearch_dsl import AsyncDocument, Text, Keyword


class NoteDoc(AsyncDocument):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    hash_link = Keyword()

    class Index:
        name = 'notes'
