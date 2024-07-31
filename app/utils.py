from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import Index


async def create_index(index_name: str, es_instance: AsyncElasticsearch, mapping: dict, ind_settings: dict):
    index = Index(index_name, using=es_instance)
    if not await index.exists():
        index.settings(**ind_settings)
        await index.create()
        await index.put_mapping(body=mapping if mapping else {})


def extract_data(data: dict):
    result = []
    for r in data['hits']['hits']:
        result.append(r['_source'])
    return result
