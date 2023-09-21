from sqlalchemy import create_engine


class Pokemon:
    _name = "Pokemon"
    client = None
    connect = None
    
    def __init__(self, client_id=False):
        self.client = create_engine(url=client_id)
        self.connect = self.client.connect()
      
    def get_random_pokemon(self):
        res = self.connect.execute("SELECT * FROM public.pokemon_table ORDER BY RANDOM() LIMIT 1")
        result = {}
        for row in res:
            for key in row.keys():
                result[key] = row[key]
        self.connect.close()
        self.client.dispose()
        return result