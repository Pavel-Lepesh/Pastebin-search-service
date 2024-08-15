from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError
from app.config import settings
from loguru import logger
from elasticsearch import AsyncElasticsearch

from app.search.documents import NoteDoc


class KafkaConsumer:
    def __init__(self):
        self.host = settings.KAFKA_HOST
        self.port = settings.KAFKA_PORT

    async def start_consume(self, es: AsyncElasticsearch):
        """
        Start consuming messages from Kafka
        and then index them in ElasticSearch.
        """
        consumer = AIOKafkaConsumer(
            "notes-1",
            bootstrap_servers=f"{self.host}:{self.port}",
            group_id="first-group")
        try:
            await consumer.start()
            logger.info("Kafka consumer is launched")
            async for msg in consumer:
                value: str = msg.value.decode()
                hash_link, title = value[:11], value[11:]  # 11 symbols - length of hash_link
                logger.info(f"Kafka consumer got a message: hash link - {hash_link} topic - {msg.topic}")

                doc = NoteDoc(**{"title": title, "hash_link": hash_link})
                response = await doc.save(using=es)

                if response == "created":
                    logger.info(f"New document \"{title}\" (hash link: {hash_link}) was created")
                else:
                    logger.error(f"Something went wrong: Document \"{title}\" (hash link: {hash_link}) wasn't created")
        except KafkaError as error:
            logger.error(f"Kafka error: {error}")
        finally:
            await consumer.stop()


kafka_consumer = KafkaConsumer()
