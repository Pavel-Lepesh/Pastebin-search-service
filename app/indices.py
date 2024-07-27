from dataclasses import dataclass
from app.mapping import NOTES_MAPPING


@dataclass
class IndexDataClass:
    index_name: str
    settings: dict
    mapping: dict


indices = [
    IndexDataClass(
        index_name='notes',
        settings={
            "number_of_shards": 5,
            "number_of_replicas": 2
        },
        mapping=NOTES_MAPPING
    )
]





