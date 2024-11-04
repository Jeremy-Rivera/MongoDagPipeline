from dagster import asset, Definitions, resource
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
    """Return a MongoDB client instance."""
    uri = context.resource_config["uri"]
    return MongoClient(uri)["mongo_persons"]

@asset(required_resource_keys={"mongo"})
def load_persons_data(context):
    """Load persons data from a JSON file into the MongoDB."""
    try:
        with open("persons.json") as f:
            persons = json.load(f)

        result = context.resources.mongo["persons"].insert_many(persons)
        context.log.info(f"Inserted {len(result.inserted_ids)} persons into MongoDB")

    except Exception as e:
        context.log.error(f"Error inserting persons into MongoDB: {e}")
        raise

defs = Definitions(
    assets=[load_persons_data],
    resources={"mongo": mongo_resource},
)

if __name__ == "__main__":
    settings = Settings()
    defs.get_job_def("__ASSET_JOB").execute_in_process(
        run_config={"resources": {"mongo": {"config": {"uri": str(settings.uri)}}}}
    )
