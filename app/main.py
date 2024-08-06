from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.search.router import router
from app.indices import indices as indices_list
from app.utils import create_index
from app.dependencies import get_elastic_client
from app.kafka import kafka_consumer
from loguru import logger
import asyncio


logger.add(
    "log_file.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file}:{line} | {message}",
    rotation="50 MB",
    level="INFO",
    enqueue=True
)

logger.add(
    "error_logs.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file}:{line} | {message}",
    rotation="50 MB",
    level="ERROR",
    enqueue=True
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await asyncio.sleep(20)
    for index in indices_list:
        await create_index(
            index_name=index.index_name,
            es_instance=await get_elastic_client(),
            mapping=index.mapping,
            ind_settings=index.settings
        )
        kafka_es_client = await get_elastic_client()
        asyncio.create_task(kafka_consumer.start_consume(kafka_es_client))
        logger.info(f"\"{index.index_name}\" index is active")
    yield


app = FastAPI(lifespan=lifespan)
app_v1 = FastAPI()


app_v1.include_router(router)
app.mount("/v1", app_v1)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
