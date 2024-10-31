from dagster import resource, op, job
from pymongo import MongoClient
from pydantic import AnyUrl
from pydantic_settings import BaseSettings
import json

class MongoDsn(AnyUrl):
    allowed_schemes = {"mongodb", "mongodb+srv"}

class Settings(BaseSettings): 
    uri: MongoDsn = MongoDsn("mongodb://127.0.0.1:27017")  

    class Config:
        env_file = ".env"

@resource(config_schema={"uri": str})
def mongo_resource(context): 
    uri = context.resource_config["uri"]
    client = MongoClient(uri)
    return client["mongo_persons"]

@op(required_resource_keys={"mongo"})
def load_persons_data(context): 
    try: 
        with open("persons.json") as f:
            persons = json.load(f)

        result = context.resources.mongo["persons"].insert_many(persons)
        context.log.info(f"Inserted {len(result.inserted_ids)} persons into MongoDB")

    except Exception as e:
        context.log.error(f"Error inserting persons into MongoDB: {e}")
        raise

@job(resource_defs={"mongo": mongo_resource})
def persons_job():
    load_persons_data()

if __name__ == "__main__":
    settings = Settings()

    persons_job.execute_in_process(
        run_config={"resources": {"mongo": {"config": {"uri": str(settings.uri)}}}}  
    )
