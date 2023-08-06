from fabric import Connection
from typing import Dict 

class ServerManager(Connection):

    def __init__(self, user:str, port: int = 22, password: str = None, connect_kwargs: Dict = None ):
        
        if not user:
            raise ClientError("Missing user arguments.")

        super(Connection, self).__init__(user, port,connect_kwargs={""})

    def login(self):
        pass 

    def install(self):
        pass
    
