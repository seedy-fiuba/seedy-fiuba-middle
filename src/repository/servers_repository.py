import os
from pymongo import MongoClient
from ..models.servers import Server


class ServerRepository(object):
    __instance = None

    def __new__(cls):
        if not ServerRepository.__instance:
            mongoclient = MongoClient(os.environ['MONGODB_URL'])
            serversdb = mongoclient.serversdb
            ServerRepository._servers = serversdb.servers
            ServerRepository._sequence = serversdb.sequence
            ServerRepository.__instance = object.__new__(cls)
            print("MongoDB servers is up")
        return ServerRepository.__instance

    def insert(self, server: Server):
        server.id = self.get_sequence()
        return self._servers.insert_one(server.dict(by_alias=True))

    def find_all(self):
        return self._servers.find()

    def find(self, params):
        return self._servers.find_one(params)

    def update_by_id(self, server_id: int, new_value: dict):
        return self._servers.find_one_and_update({'_id': server_id}, new_value)

    def get_sequence(self):
        document = self._sequence.find_one_and_update({"_id": 'server'}, {"$inc": {"value": 1}}, return_document=True)
        if document is None:
            document = {"_id": 'server', "value": 0}
            self._sequence.insert_one(document)

        return document["value"]
