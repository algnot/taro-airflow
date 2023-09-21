from sqlalchemy import create_engine
from config import Config


class Base:
    client = None
    connect = None
    config = None
    
    def __init__(self):
        self.config = Config()
        
    def execute(self, query):
        self.client = create_engine(url=self.config.get("POSTGRES_URL"))
        self.connect = self.client.connect()
        res = self.connect.execute(query)
        result = {}
        
        for row in res:
            for key in row.keys():
                result[key] = row[key]
                
        self.connect.close()
        self.client.dispose()
        return result