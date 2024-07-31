from elasticsearch import AsyncElasticsearch
from elastic_transport import ConnectionError
from app.config import settings
from fastapi import HTTPException


async def get_elastic_client() -> AsyncElasticsearch:
    try:
        client = AsyncElasticsearch(
            [{'host': settings.ES_HOST, 'port': settings.ES_PORT, 'scheme': settings.ES_SCHEME}],
            verify_certs=False,
            ssl_show_warn=False,
        )
        if not await client.ping():
            raise ConnectionError("Elastic connection error")
        return client
    except ConnectionError:
        raise HTTPException(status_code=500, detail="Elastic connection error")
