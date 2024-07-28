from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.exceptions import ResponseValidationError
from pydantic import ValidationError

from app.search.schemas import NoteScheme, IndexResponseScheme
from elasticsearch import AsyncElasticsearch
from typing import Annotated
from app.dependencies import get_elastic_client
from app.search.documents import NoteDoc


router = APIRouter(
    prefix='/search',
)


@router.post("/create_doc", status_code=status.HTTP_201_CREATED)
async def root(body: NoteScheme, es: Annotated[AsyncElasticsearch, Depends(get_elastic_client)]) -> IndexResponseScheme:
    try:
        doc = NoteDoc(**body.dict())
        response = await doc.save(using=es)
        return IndexResponseScheme(**{"operation_result": response})
    except ResponseValidationError:
        raise HTTPException(status_code=500, detail="Elastic indexing response error")
