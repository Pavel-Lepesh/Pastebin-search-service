from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.exceptions import ResponseValidationError

from app.search.schemas import NoteScheme, IndexResponseScheme
from elasticsearch import AsyncElasticsearch
from elasticsearch_dsl import AsyncSearch
from typing import Annotated
from app.dependencies import get_elastic_client
from app.search.documents import NoteDoc
from app.utils import extract_data


router = APIRouter(
    prefix='/search',
)


@router.post("/create_doc", status_code=status.HTTP_201_CREATED)
async def create_document(body: NoteScheme, es: Annotated[AsyncElasticsearch, Depends(get_elastic_client)]) -> IndexResponseScheme:
    try:
        doc = NoteDoc(**body.dict())
        response = await doc.save(using=es)
        return IndexResponseScheme(**{"operation_result": response})
    except ResponseValidationError:
        raise HTTPException(status_code=500, detail="Elastic indexing response error")


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
