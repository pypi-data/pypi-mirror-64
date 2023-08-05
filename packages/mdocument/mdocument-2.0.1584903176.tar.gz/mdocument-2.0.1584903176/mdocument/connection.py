import urllib.parse

from motor.motor_asyncio import AsyncIOMotorClient


class DatabaseClient:
    def __init__(self, uri: str = None, replica_set: list = None, host: str = None,
                 username: str = None, password: str = None, auth_database: str = "admin"):

        if uri:
            self.client = AsyncIOMotorClient(uri)
        else:
            if replica_set:
                host = ",".join(replica_set)

            if not username or not password:
                uri = f"mongodb://{host}"
            else:
                username = urllib.parse.quote_plus(username)
                password = urllib.parse.quote_plus(password)
                uri = f"mongodb://{username}:{password}@{host}/{auth_database}"

            self.client = AsyncIOMotorClient(uri)
