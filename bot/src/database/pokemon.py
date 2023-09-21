from sqlalchemy import create_engine
from .base import Base

class Pokemon (Base):
    _name = "Pokemon"
    
    def __init__(self):
        super().__init__()
      
    def get_random_pokemon(self):
        return self.execute("SELECT * FROM public.pokemon_table ORDER BY RANDOM() LIMIT 1")
