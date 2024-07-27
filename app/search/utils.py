from fastapi import HTTPException
from app.search.schemas import NoteScheme
from elasticsearch import AsyncElasticsearch


async def index_note(note: NoteScheme, es: AsyncElasticsearch):
    try:
        await es.index(index='notes', document=note.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка при индексации документа")