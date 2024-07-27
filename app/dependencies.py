from elasticsearch import AsyncElasticsearch
from app.config import settings


async def get_elastic_client() -> AsyncElasticsearch:
    return AsyncElasticsearch([{'host': settings.ES_HOST, 'port': settings.ES_PORT, 'scheme': settings.ES_SCHEME}])
