from fastapi import APIRouter, Depends, status, HTTPException, Query, Path
from fastapi.exceptions import ResponseValidationError

from app.search.schemas import NoteScheme, IndexResponseScheme
from elasticsearch import AsyncElasticsearch
from elastic_transport import ConnectionError
from elasticsearch_dsl import AsyncSearch
from typing import Annotated
from app.dependencies import get_elastic_client
from app.search.documents import NoteDoc
from app.utils import extract_data
from loguru import logger


router = APIRouter(
    prefix='/search',
)


@router.post("/create_doc", status_code=status.HTTP_201_CREATED)
async def create_document(body: NoteScheme, es: Annotated[AsyncElasticsearch, Depends(get_elastic_client)]) -> IndexResponseScheme:
    try:
        doc = NoteDoc(**body.dict())
        response = await doc.save(using=es)
        logger.info(f"New document \"{body.title}\" (hash link: {body.hash_link}) was created")
        return IndexResponseScheme(**{"operation_result": response})
    except ResponseValidationError:
        raise HTTPException(status_code=500, detail="Elastic indexing response error")


@router.put("/update_doc/{hash_link}", status_code=status.HTTP_201_CREATED)
async def update_document(hash_link: Annotated[str, Path(max_length=11)],
                          title: Annotated[str, Query(max_length=100)],
                          es: Annotated[AsyncElasticsearch, Depends(get_elastic_client)]):
    try:
        query_dict = {
            "query": {
                "term": {
                    "hash_link": hash_link
                }
            }
        }
        search = AsyncSearch(using=es, index="notes")
        search.update_from_dict(query_dict)
        search_result = await search.execute()

        data: list = extract_data(search_result.to_dict(), only_ids=True)
        logger.info(f"search data: {data}")
        if not data:
            raise HTTPException(404, "Document not found")
        if len(data) > 1:
            logger.error(f"There is more than one document with a hash link: {hash_link}")
        await es.update(
            index="notes",
            id=data[0],
            doc={
                "title": title
            }
        )
    except ConnectionError as error:
        logger.error(error)
        raise HTTPException(500, "Connection error")


@router.get("/search", status_code=status.HTTP_200_OK)
async def main_search(query: Annotated[str, Query(max_length=255)],
                      es: Annotated[AsyncElasticsearch, Depends(get_elastic_client)]) -> list[NoteScheme]:
    query_dict = {
        "query": {
            "match": {
                "title": {
                    "query": query,
                    "fuzziness": "AUTO"
                }
            }
        }
    }
    search = AsyncSearch(using=es, index='notes')
    search.update_from_dict(query_dict)
    result = await search.execute()
    return extract_data(result.to_dict())


@router.delete("/delete_doc/{hash_link}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(hash_link: str, es: Annotated[AsyncElasticsearch, Depends(get_elastic_client)]):
    query_dict = {
        "query": {
            "term": {
                "hash_link": hash_link
            }
        }
    }
    search = AsyncSearch(using=es, index='notes')
    search.update_from_dict(query_dict)
    await search.delete()
    logger.info(f"Document (hash link: {hash_link}) was deleted")
