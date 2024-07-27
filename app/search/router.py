from fastapi import APIRouter, Depends
from app.search.schemas import NoteScheme
from elasticsearch import AsyncElasticsearch
from typing import Annotated
from app.dependencies import get_elastic_client
from app.search.utils import index_note


router = APIRouter(
    prefix='/search',
)


@router.post("/create_doc")
async def root(body: NoteScheme, es: Annotated[AsyncElasticsearch, Depends(get_elastic_client)]):
    await index_note(body, es)
    return "success"
