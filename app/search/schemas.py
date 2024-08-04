from pydantic import BaseModel, Field


class NoteScheme(BaseModel):
    title: str = Field(max_length=255)
    hash_link: str = Field(max_length=11)


class IndexResponseScheme(BaseModel):
    operation_result: str
