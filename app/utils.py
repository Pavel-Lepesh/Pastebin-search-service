from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import Index
from loguru import logger


async def create_index(index_name: str, es_instance: AsyncElasticsearch, mapping: dict, ind_settings: dict):
    index = Index(index_name, using=es_instance)
    if not await index.exists():
        index.settings(**ind_settings)
        await index.create()
        await index.put_mapping(body=mapping if mapping else {})
        logger.info(f"\"{index_name}\" index was created")
    else:
        logger.info(f"\"{index_name}\" index already exists")


def extract_data(data: dict, only_ids=False) -> list:
    """
    Allows to implicitly extract data from an ElasticSearch response.
    """
    result = []
    if only_ids:
        for r in data['hits']['hits']:
            result.append(r['_id'])
    else:
        for r in data['hits']['hits']:
            result.append(r['_source'])
    return result
