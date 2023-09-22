from sqlalchemy import create_engine
from config import Config


class Base:
    client = None
    connect = None
    config = None
    
    def __init__(self):
        self.config = Config()
        
    def execute(self, query):
        try:
            self.client = create_engine(url=self.config.get("POSTGRES_URL"))
            self.connect = self.client.connect()
            res = self.connect.execute(query)
            results = []
            
            if not res:
                self.connect.close()
                self.client.dispose()
                return []
            
            for row in res:
                result = {}
                for key in row.keys():
                    result[key] = row[key]
                results.append(result)
                    
            self.connect.close()
            self.client.dispose()
            return results  
        
        except Exception:
            self.connect.close()
            self.client.dispose()
            return []
            
            
        